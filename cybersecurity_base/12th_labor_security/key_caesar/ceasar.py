import re

from .enums import Letters
from .exceptions import BadStep, BadWord


class CaesarWithWord:
    def __init__(self, key: str, step: int):
        self.key = key
        self._step = step

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not (re.fullmatch(r"[а-яё]+", value, re.I) and self._step < 33):
            raise BadStep("Неправильное значение шага. В русском алфавите 33 буквы.")
        if not (re.fullmatch(r"[a-z]+", value, re.I) and self._step < 26):
            raise BadStep("Неправильное значение шага. В английском алфавите 26 букв.")
        if any(map(lambda x: x.isspace(), value.strip())):
            raise BadWord("Ключ может состоять только из одного слова")
        self._key = ''.join(set(value))

    def encode(self, string: str):
        tmp: str = ''.join(word for word in self._get_language(string) if word not in self.key)
        alpha_new: str = tmp[-self._step:] + self.key + tmp[:-self._step]
        return string.translate(str.maketrans(self._get_language(string), alpha_new))

    @staticmethod
    def _get_language(string):
        words = re.findall(r'\w+', string, re.UNICODE)
        if all(re.fullmatch(r"^[a-z]+$", word) for word in words):
            return Letters.ENGLISH_SYMBOLS_LOWER.value
        if all(re.fullmatch(r"^[A-Z]+$", word) for word in words):
            return Letters.ENGLISH_SYMBOLS_UPPER.value
        if all(re.fullmatch(r"^[а-яё]+$", word) for word in words):
            return Letters.RUSSIAN_SYMBOLS_LOWER.value
        if all(re.fullmatch(r"^[А-ЯЁ]+$", word) for word in words):
            return Letters.RUSSIAN_SYMBOLS_UPPER.value
