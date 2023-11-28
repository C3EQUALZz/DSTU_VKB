"""
Здесь реализована логика шифра "Аффинная система подстановок Цезаря"
"""

import math
import re
from typing import NoReturn

from .exceptions import NotValidNumbers, NoSupport

from python_language.cybersecurity_base.twelve_labor_security.abstract_class_cyphers import Cypher


class Affine(Cypher):
    """
    Класс реализует аффинный шифр.

    Args:
        key: tuple[int, int] - содержит числовые значения коэффициентов a и b
    """
    __slots__ = ("_key", "m")

    def __init__(self, key: tuple[int, ...]):
        self.key = key
        self.m = None

    @property
    def key(self) -> tuple[int, int]:
        """
        Свойство для получения значения ключа.

        Returns:
            tuple[int, int]: Кортеж с числовыми значениями коэффициентов a и b
        """
        return self._key

    @key.setter
    def key(self, values: tuple) -> None:
        """
        Сеттер для установки значения ключа.

        Args:
            values (tuple): Кортеж с числовыми значениями коэффициентов a и b

        Raises:
            NotValidNumbers: Если переданные значения не являются целыми числами
        """
        if not all(isinstance(x, int) for x in values):
            raise NotValidNumbers("Не целые числа передаются")
        self._key = values

    def _length_abc(self, sentence: str) -> int | NoReturn:
        """
        Метод определяет длину алфавита в зависимости от ввода.

        Args:
            sentence (str): Строка, которую ввел пользователь

        Returns:
            int | NoSupport: Длина алфавита или исключение, если язык не поддерживается
        """
        if not(math.gcd(self.key[0], 26) == 1 or math.gcd(self.key[0], 33) == 1):
            raise ValueError("Не взаимно простые числа a и количество букв в алфавите ")

        words = re.findall(r'\w+', sentence, re.UNICODE)
        if (all(re.fullmatch(r"^[a-z]+$", word, re.I) for word in words)
                and math.gcd(self.key[0], 26) == 1):
            return 26

        if (all(re.fullmatch(r"^[а-яё]+$", word, re.I) for word in words)
                and math.gcd(self.key[0], 33) == 1):
            return 33
        raise NoSupport("Используется неподдерживаемый язык")

    def _encrypt_char(self, t: str):
        """
        Метод шифрует символ.

        Args:
            t (str): Символ

        Returns:
            str: Зашифрованный символ
        """
        if not t.isalpha():
            return t

        # a, b = self.key не рабочий вариант для кириллицы из-за буквы ё
        # alphabet_start = self._get_alphabet_starting_point(t)
        # encrypted_char = (a * (ord(t) - alphabet_start) + b) % self.m
        # return chr(alphabet_start + encrypted_char)

        a, b = self.key
        return Affine._get_language(t)[((a * Affine._get_language(t).find(t) + b) % self.m)]

    def encrypt(self, string: str):
        """
        Метод шифрует строку.

        Args:
            string (str): Строка для шифрования

        Returns:
            str: Зашифрованная строка
        """
        self.m = self._length_abc(string)
        return "".join(map(self._encrypt_char, string))

    def _decrypt_char(self, t: str):
        """
        Метод дешифрует символ.

        Args:
            t (str): Зашифрованный символ

        Returns:
            str: Расшифрованный символ
        """
        if not t.isalpha():
            return t

        a, b = self.key
        return Affine._get_language(t)[self._find_modular_inverse(a) * (Affine._get_language(t).find(t) - b) % self.m]

    def decrypt(self, string):
        """
        Метод дешифрует строку.

        Args:
            string (str): Зашифрованная строка

        Returns:
            str: Расшифрованная строка
        """
        self.m = self._length_abc(string)
        return "".join(map(self._decrypt_char, string))

    def _find_modular_inverse(self, t) -> int | None:
        """
        Метод находит модульный обратный элемент.

        Args:
            t (int): Значение для нахождения обратного элемента
        """
        for i in range(self.m):
            if ((t % self.m) * (i % self.m)) % self.m == 1:
                return i
        return None
