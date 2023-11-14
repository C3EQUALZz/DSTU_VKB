"""
Здесь логика обычного шифра Цезаря

"""
from .enums import Letters
from .exceptions import NoSupport
import re


class CaesarCipher:
    def __init__(self, key: int):
        self._key: int = key

    def _encode_abc(self, text) -> dict[int] | NoSupport:
        abc: None | dict[int] = None

        if re.search(r"[а-яА-Я]+", text):
            abc = str.maketrans(Letters.RUSSIAN_SYMBOLS_LOWER.value,
                                Letters.RUSSIAN_SYMBOLS_LOWER.value[self._key:] +
                                Letters.RUSSIAN_SYMBOLS_LOWER.value[:self._key]) \
                  | str.maketrans(Letters.RUSSIAN_SYMBOLS_UPPER.value,
                                  Letters.RUSSIAN_SYMBOLS_UPPER.value[self._key:] +
                                  Letters.RUSSIAN_SYMBOLS_UPPER.value[:self._key])

        elif re.search(r"[a-zA-Z]", text):
            abc = str.maketrans(Letters.ENGLISH_SYMBOLS_LOWER.value,
                                Letters.ENGLISH_SYMBOLS_LOWER.value[self._key:] +
                                Letters.ENGLISH_SYMBOLS_LOWER.value[:self._key]) \
                  | str.maketrans(Letters.ENGLISH_SYMBOLS_UPPER.value,
                                  Letters.ENGLISH_SYMBOLS_UPPER.value[self._key:] +
                                  Letters.ENGLISH_SYMBOLS_UPPER.value[:self._key])

        if abc is None:
            raise NoSupport("Не добавлена поддержка данного языка")
        return abc

    def encode(self, string: str) -> str:
        return str.translate(string, self._encode_abc(string))

    def decode(self, string: str) -> str:
        return str.translate(string, {v: k for k, v in self._encode_abc(string).items()})
