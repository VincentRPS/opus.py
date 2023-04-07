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


class OpusException(Exception):
    """An error raised by the Opus library."""


class CException(Exception):
    """An error raised by, or related to, the C library."""


def raise_c_err(num: int) -> None:
    if num == -1:
        raise CException("Bad Argument")
    elif num == -2:
        raise CException("Buffer too small")
    elif num == -3:
        raise CException("Internal Error")
    elif num == -4:
        raise CException("Invalid Packet")
    elif num == -5:
        raise CException("Unimplemented")
    elif num == -6:
        raise CException("Invalid State")
    elif num == -7:
        raise CException("Allocation Failed")
