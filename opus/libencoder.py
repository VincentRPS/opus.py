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
from typing import Sequence

from .c_lib import get_lib
from .types import EncoderStructPtr, c_float_ptr, c_int16_ptr, c_int32_ptr, c_int_ptr


class EncoderFuncs:
    """Typing for libopus encoder functions."""

    def encode(
        self,
        encoder: EncoderStructPtr,
        pcm: c_int16_ptr,
        frame_size: ctypes.c_int,
        data: ctypes.c_char_p,
        max_data_bytes: ctypes.c_int32,
    ) -> ctypes.c_int32:
        ...

    def encode_float(
        self,
        encoder: EncoderStructPtr,
        pcm: c_float_ptr,
        frame_size: ctypes.c_int,
        data: ctypes.c_char_p,
        max_data_bytes: ctypes.c_int32,
    ) -> ctypes.c_int32:
        ...

    def ctl(self) -> ctypes.c_int32:
        ...

    def destroy(self, st: EncoderStructPtr) -> None:
        ...

    def get_size(self, channels: ctypes.c_int) -> ctypes.c_int:
        ...

    def create(
        self,
        samping_rate: ctypes.c_int,
        channels: ctypes.c_int,
        mode: ctypes.c_int,
        error: c_int_ptr,
    ) -> EncoderStructPtr:
        ...

    def init(
        self,
        encoder: EncoderStructPtr,
        fs: c_int32_ptr,
        channels: ctypes.c_int,
        application: ctypes.c_int,
    ) -> None:
        ...

    def get_size(self, channels: ctypes.c_int) -> ctypes.c_int:
        ...

    def create(
        self,
        fs: c_int32_ptr,
        channels: ctypes.c_int,
        application: ctypes.c_int,
        error: c_int_ptr,
    ) -> EncoderStructPtr:
        ...


class LibEncoder(EncoderFuncs):
    ___EXPORTED: Sequence[str] = (
        "opus_encode",
        "opus_encode_float",
        "opus_encoder_ctl",
        "opus_encoder_destroy",
        "opus_encoder_get_size",
        "opus_encoder_create",
        "opus_encoder_init",
    )

    def __init__(self) -> None:
        lib = get_lib()

        for exp in self.___EXPORTED:
            name = exp.removeprefix("opus")

            if name.startswith("_encoder"):
                name = name.removeprefix("_encoder_")
            else:
                name = name.removeprefix("_")

            setattr(self, name, getattr(lib, exp))
