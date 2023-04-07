"""
MIT License

Copyright (c) 2023 VincentRPS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import array
import ctypes
import math
from typing import Literal

from .error import CException, OpusException
from .libdecoder import LibDecoder
from .types import CTL, SAMPLE_RATE, c_int16_ptr, c_int32_ptr


class Decoder:
    """High-level Python bindings for Opus

    Parameters
    ----------
    samples: SAMPLE_RATE
        The integer sample rate.
        Defaults to Opus' recommended `4800`.
    channels: Literal[1, 2]
        The amount of channels to use to decode.
        Defaults to `1`.
    """

    def __init__(
        self, samples: SAMPLE_RATE = 4800, channels: Literal[1, 2] = 1
    ) -> None:
        self.lib = LibDecoder()
        err = ctypes.c_int()
        self.channels = channels
        self.samples = samples
        self.samples_per_frame = int(samples / 1000 * 20)
        self.___ptr = self.lib.create(
            ctypes.cast(samples, c_int32_ptr), ctypes.c_int(channels), ctypes.byref(err)
        )
        if err.value != 0:
            raise CException(self.lib.strerror(err))

    def get_size(self) -> int:
        return self.lib.get_size(self.channels).value

    def set_gain(self, dB: int) -> None:
        """Set the gain for decoding in decibels.

        Parameters
        ----------
        dB: :class:`int`
            The gain in decibels.
        """

        dB_Q8 = max(-32768, min(32767, round(dB * 256)))
        self.lib.ctl(self.___ptr, CTL.SET_GAIN.value, dB_Q8)

    def get_last_packet_duration(self) -> int:
        """Acquire the duration of the last packet"""

        ret = ctypes.c_int32()
        self.lib.ctl(self.___ptr, CTL.SET_GAIN.value, ctypes.byref(ret))
        return ret.value

    def set_volume(self, mult: int | float):
        """Set an output volume as a percentage such as 1%, 50%, etc.

        Parameters
        ----------
        mult: int | float
            The percentage to set the volume as.
        """

        return self.set_gain(20 * math.log10(mult))  # amplitude ratio

    def decode(self, data: bytes, fec: int | None = None) -> bytes:
        if data is None and fec:
            raise OpusException("data cannot be null with fec present")

        if data is None:
            frame_size = self.get_last_packet_duration() or self.samples_per_frame
        else:
            frames = self.lib.packet_get_nb_frames(data, len(data))
            samples_per_frame = self.lib.packet_get_samples_per_frame(data)
            frame_size = frames * samples_per_frame

        pcm = (
            ctypes.c_int16
            * (frame_size * self.channels * ctypes.sizeof(ctypes.c_int16))
        )()
        pcm_ptr = ctypes.cast(pcm, c_int16_ptr)

        ret = self.lib.decode(
            self.___ptr, data, len(data) if data else 0, pcm_ptr, frame_size, fec
        )

        return array.array("h", pcm[: ret * self.channels]).tobytes()
