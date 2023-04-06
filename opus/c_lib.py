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


import ctypes.util
import functools
import os
import struct
import sys
from ctypes import cdll

from .error import OpusException


@functools.cache
def get_lib():
    try:
        if sys.platform == "win32":
            basedir = os.path.dirname(os.path.abspath(__file__))
            bitness = struct.calcsize("P") * 8
            target = "x64" if bitness > 32 else "x86"
            path = os.path.join(basedir, "bin", f"libopus-0.{target}.dll")
        else:
            path = ctypes.util.find_library("opus")
    except Exception as exc:
        raise OpusException(
            f"Unable to find Opus library (if you're encountering this error, it may be because \
            you don't have Opus! make sure to download Opus: https://opus-codec.org) error result: {exc}"
        )

    return cdll.LoadLibrary(path)
