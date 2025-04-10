"""
Создаю абстрактный класс, чтобы учитывался полиморфизм для каждого класса
"""

import re
from abc import ABC, abstractmethod

from .enums import Letters


class Cypher(ABC):
    @abstractmethod
    def encrypt(self, *args, **kwargs): ...

    @abstractmethod
    def decrypt(self, *args, **kwargs): ...

    @staticmethod
    def _get_language(string):
        words = re.findall(r"\w+", string, re.UNICODE)
        if all(re.fullmatch(r"^[a-z]+$", word) for word in words):
            return Letters.ENGLISH_SYMBOLS_LOWER.value
        if all(re.fullmatch(r"^[а-яё]+$", word) for word in words):
            return Letters.RUSSIAN_SYMBOLS_LOWER.value
        if all(re.fullmatch(r"^[A-Z]+$", word) for word in words):
            return Letters.ENGLISH_SYMBOLS_UPPER.value
        if all(re.fullmatch(r"^[А-ЯЁ]+$", word) for word in words):
            return Letters.RUSSIAN_SYMBOLS_UPPER.value
