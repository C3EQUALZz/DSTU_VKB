"""
Здесь реализована логика шифра "Аффинная система подстановок Цезаря"
"""

import math
import re
from typing import NoReturn

from .exceptions import NotValidNumbers, NoSupport


class Affine:
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
        words = re.findall(r'\w+', sentence, re.UNICODE)
        if (all(re.fullmatch(r"^[a-z]+$", word, re.I) for word in words)
                and math.gcd(self.key[0], 26) == 1):
            return 26

        if (all(re.fullmatch(r"^[а-яё]+$", word, re.I) for word in words)
                and math.gcd(self.key[0], 33) == 1):
            return 33
        raise NoSupport("Используется неподдерживаемый язык")

    def _get_alphabet_starting_point(self, alpha: str):
        """
        Метод возвращает начальную точку алфавита для символа.

        Args:
            alpha (str): Символ

        Returns:
            int: Начальная точка алфавита для символа
        """
        # маленькая русская буква
        if alpha.islower() and self.m == 33:
            return ord("а")
        # большая русская буква
        if alpha.isupper() and self.m == 33:
            return ord("А")
        # маленькая английская буква
        if alpha.islower() and self.m == 26:
            return ord("a")
        # большая английская буква
        if alpha.isupper() and self.m == 26:
            return ord("A")

    def _encrypt_char(self, t: str):
        """
        Метод шифрует символ.

        Args:
            t (str): Символ

        Returns:
            str: Зашифрованный символ
        """
        if t.isspace():
            return " "

        a, b = self.key
        return chr(self._get_alphabet_starting_point(t) +
                   (a * (ord(t) - self._get_alphabet_starting_point(t)) + b) % self.m)

    def encrypt(self, string):
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
        if t.isspace():
            return " "

        a, b = self.key
        return chr(self._get_alphabet_starting_point(t) +
                   self._find_modular_inverse(a) * (ord(t) - self._get_alphabet_starting_point(t) - b) % self.m)

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
