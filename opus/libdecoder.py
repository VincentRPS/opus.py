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


import ctypes
from typing import Any, Sequence

from .c_lib import get_lib
from .types import DecoderStructPtr, c_float_ptr, c_int16_ptr, c_int32_ptr, c_int_ptr


class DecoderFuncs:
    def get_size(self, channels: ctypes.c_int) -> ctypes.c_int:
        ...

    def strerror(self, error: ctypes.c_int) -> ctypes.c_char:
        ...

    def init(
        self, decoder: DecoderStructPtr, fs: c_int32_ptr, channels: ctypes.c_int
    ) -> ctypes.c_int:
        ...

    def decode(
        self,
        decoder: DecoderStructPtr,
        data: ctypes.c_char_p,
        len: c_int32_ptr,
        pcm: c_int16_ptr,
        frame_size: ctypes.c_int,
        decode_fec: ctypes.c_int,
    ) -> ctypes.c_int:
        ...

    def decode_float(
        self,
        decoder: DecoderStructPtr,
        data: ctypes.c_char_p,
        len: c_int32_ptr,
        pcm: c_float_ptr,
        frame_size: ctypes.c_int,
        decode_fec: ctypes.c_int,
    ) -> ctypes.c_int:
        ...

    def create(
        self, fs: c_int32_ptr, channels: ctypes.c_int, error: c_int_ptr
    ) -> DecoderStructPtr:
        ...

    def ctl(
        self, decoder: DecoderStructPtr, request: ctypes.c_int, *args: Any
    ) -> ctypes.c_int:
        ...

    def destroy(self, decoder: DecoderStructPtr) -> None:
        ...

    def get_samples_per_frame(
        self, data: ctypes.c_char_p, fs: c_int32_ptr
    ) -> ctypes.c_int:
        ...

    def packet_get_bandwidth(self, data: ctypes.c_char_p) -> ctypes.c_int:
        ...

    def packet_get_nb_channels(self, data: ctypes.c_char_p) -> ctypes.c_int:
        ...

    def packet_get_nb_frames(
        self, data: ctypes.c_char_p, len: c_int32_ptr
    ) -> ctypes.c_int:
        ...

    def packet_get_nb_samples(
        self,
        decoder: DecoderStructPtr,
        packet: ctypes.c_char_p,
        len: c_int32_ptr,
        fs: c_int32_ptr,
    ) -> ctypes.c_int:
        ...

    def packet_get_samples_per_frame(
        self, data: ctypes.c_char_p, fs: c_int32_ptr
    ) -> ctypes.c_int:
        ...

    def get_nb_samples(
        self,
        decoder: DecoderStructPtr,
        packet: ctypes.c_char_p,
        len: c_int32_ptr,
        fs: c_int32_ptr,
    ) -> ctypes.c_int:
        ...

    def packet_parse(
        self,
        data: ctypes.c_char_p,
        len: c_int32_ptr,
        out_toc: ctypes.c_char_p,
        frames: ctypes.c_char_p,
        size: c_int16_ptr,
        payload_offset: c_int_ptr,
    ) -> ctypes.c_int:
        ...

    def pcm_soft_clip(
        self,
        pcm: c_float_ptr,
        frame_size: ctypes.c_int,
        channels: ctypes.c_int,
        softclip_mem: c_float_ptr,
    ) -> None:
        ...


class LibDecoder(DecoderFuncs):
    ___EXPORTED: Sequence[str] = (
        "opus_decode",
        "opus_decode_float",
        "opus_decoder_ctl",
        "opus_decoder_destroy",
        "opus_decoder_get_size",
        "opus_decoder_create",
        "opus_decoder_init",
        "opus_decoder",
        "opus_decoder_get_samples_per_frame",
        "opus_packet_parse",
        "opus_packet_get_bandwidth",
        "opus_packet_get_nb_channels",
        "opus_packet_get_nb_frames",
        "opus_packet_get_nb_samples",
        "opus_packet_get_samples_per_frame",
        "opus_decoder_get_nb_samples",
        "opus_pcm_soft_clip",
    )

    def __init__(self) -> None:
        lib = get_lib()

        for exp in self.___EXPORTED:
            name = exp.removeprefix("opus")

            if name.startswith("_decoder"):
                name = name.removeprefix("_decoder_")
            else:
                name = name.removeprefix("_")

            setattr(self, name, getattr(lib, exp))
