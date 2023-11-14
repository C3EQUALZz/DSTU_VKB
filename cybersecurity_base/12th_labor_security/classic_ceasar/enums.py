"""
Здесь находятся перечисления, которые улучшают читабельность кода
"""
from string import ascii_lowercase as low, ascii_uppercase as up
from enum import Enum


class Letters(Enum):
    RUSSIAN_SYMBOLS_LOWER: str = ''.join(
        [chr(i) for i in range(1072, 1072 + 6)] +
        [chr(1072 + 33)] +
        [chr(i) for i in range(1072 + 6, 1072 + 32)]
    )

    RUSSIAN_SYMBOLS_UPPER: str = ''.join(
        [chr(i) for i in range(1040, 1040 + 6)] +
        [chr(1025)] +
        [chr(i) for i in range(1040 + 6, 1040 + 32)]
    )
    ENGLISH_SYMBOLS_LOWER: str = low
    ENGLISH_SYMBOLS_UPPER: str = up
