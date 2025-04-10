"""
Здесь находятся перечисления, которые улучшают читабельность кода
"""

__all__ = ["Letters"]

from enum import Enum
from string import ascii_lowercase as low
from string import ascii_uppercase as up


class Letters(Enum):
    RUSSIAN_SYMBOLS_LOWER: str = "".join(
        [chr(i) for i in range(1072, 1072 + 6)]
        + [chr(1072 + 33)]
        + [chr(i) for i in range(1072 + 6, 1072 + 32)]
    )

    RUSSIAN_SYMBOLS_UPPER: str = "".join(
        [chr(i) for i in range(1040, 1040 + 6)]
        + [chr(1025)]
        + [chr(i) for i in range(1040 + 6, 1040 + 32)]
    )
    ENGLISH_SYMBOLS_LOWER: str = low
    ENGLISH_SYMBOLS_UPPER: str = up
