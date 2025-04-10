"""
Здесь реализован класс, который обрабатывает шифр Триземуса
"""

import re
from functools import reduce

from cybersecurity_base.twelfth_laboratory.abstract_class_cyphers import Cypher


class TrisemusCipher(Cypher):
    """
    Класс, где описана реализация шифра Триземуса
    """

    def __init__(self, key: str, table_sizes: str):
        # ключ шифрования
        self.key = key
        # аргумент, который передает пользователь для размера таблицы
        self.table_sizes = re.split(r"x|,|\s", table_sizes)
        # высчитываем размер таблицы, сделал заумно зачем-то
        self.size = reduce(lambda x, y: int(x) * int(y), self.table_sizes, 1)

    def encrypt(self, string: str) -> str:
        """
        Метод, который шифрует строку, введенную пользователем.
        :param string: Строка, которую пользователь хочет зашифровать.
        :return: Зашифрованная строка
        """
        # Создаем нашу строку-ключ, которая является началом таблицы
        key = "".join(sorted(set(self.key), key=self.key.index))
        # Создаем нашу таблицу перевода
        table = (key + "".join(x for x in self._get_language(string) if x not in key))[
            : self.size
        ]
        # Склеивание строки, которую мы перевели
        return "".join(
            self._encode_symbol(x, table) if x.isalpha() else x for x in string
        )

    def decrypt(self, string: str) -> str:
        """
        Метод, который может расшифровать строку, введенную пользователем.
        :param string: Строка, которую пользователь хочет расшифровать.
        :return: Расшифрованная строка.
        """
        key = "".join(sorted(set(self.key), key=self.key.index))
        table = (key + "".join(x for x in self._get_language(string) if x not in key))[
            : self.size
        ]
        return "".join(
            self._decode_symbol(x, table) if x.isalpha() else x for x in string
        )

    def _encode_symbol(self, char: str, table: str) -> str:
        """
        Таблица, по которой мы будем проводить шифрование.
        Здесь реализован сдвиг вниз по колонке, но у меня же одна строка, а не целая таблица.
        :param char: Буква, которую мы хотим изменить.
        :param table: Таблица, по которой мы проводим шифрование, в моем случае - это строка.
        :return: Новая буква, полученная путем сдвига.
        """
        return table[(table.find(char) + int(self.table_sizes[-1])) % len(table)]

    def _decode_symbol(self, char: str, table: str) -> str:
        """
        Здесь реализована расшифровка с использованием таблицы Триземуса.
        Тоже высчитывается по формуле.
        :param char: Буква, которую мы хотим изменить.
        :param table: Таблица, по которой мы проводим расшифрование, в моем случае - это строка.
        :return: Новая буква, полученная путем сдвига.
        """
        return table[(table.find(char) - int(self.table_sizes[-1])) % len(table)]
