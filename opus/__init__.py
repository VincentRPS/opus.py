"""
Opus
~~~~
Opus Python Wrapper.

:license: MIT
:copyright: 2023 VincentRPS
"""

from typing import Sequence

from .libencoder import *

__all__: Sequence[str] = ("LibEncoder", "LibDecoder")
