import re

from cybersecurity_base.twelfth_laboratory.abstract_class_cyphers import Cypher

from .exceptions import BadStep, BadWord


class CaesarWithWord(Cypher):
    """
    Класс, который отвечает за шифрование с использованием шифра Цезаря, учитывая подстановку.
    :param key: Ключевое слово
    :param step: Старт, с которого начнется заполнение таблицы
    """

    def __init__(self, key: str, step: int):
        self._step = step
        self.key = key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        """
        Свойство, которое используется для проверки нашего составного ключа.
        В каждом алфавите разное количество букв, поэтому стоит такая затычка в качестве проверки.
        :param value: Слово, которым мы будем шифровать.
        :return: Ничего не возвращает, устанавливает значение в атрибут
        """
        if re.fullmatch(r"[а-яё]+", value, re.I) and self._step >= 33:
            raise BadStep("Неправильное значение шага. В русском алфавите 33 буквы.")
        if re.fullmatch(r"[a-z]+", value, re.I) and self._step >= 26:
            raise BadStep("Неправильное значение шага. В английском алфавите 26 букв.")
        if any(map(lambda x: x.isspace(), value.strip())):
            raise BadWord("Ключ может состоять только из одного слова")
        self._key = "".join(set(value))

    def encrypt(self, string: str) -> str:
        """
        Метод, который шифрует наше сообщение.
        :param string: Строка, которую ввел пользователь для шифрования.
        :return: Строка, которая была зашифрована.
        """
        # Наш словарь - строка, в котором мы будем хранить буквы для шифрования.
        # Мы его заполняем от самого начала, поэтому есть проверка, что надо добавлять буквы, которых
        # нет в ключе
        tmp: str = "".join(
            word for word in self._get_language(string) if word not in self.key
        )
        # Беру с конца словарь букв, как в примере, потом добавляю слово, а потом уже оставшиеся буквы
        alpha_new: str = tmp[-self._step :] + self.key + tmp[: -self._step]
        return string.translate(str.maketrans(self._get_language(string), alpha_new))

    def decrypt(self, string: str) -> str:
        """
        Метод, который может расшифровать сообщение.
        :param string: Строка, которую ввел пользователь для расшифровки.
        :return: Строка, которая была расшифрована.
        """
        # Наш словарь - строка, в котором мы будем хранить буквы для шифрования.
        # Мы его заполняем от самого начала, поэтому есть проверка, что надо добавлять буквы, которых
        # нет в ключе
        tmp: str = "".join(
            word for word in self._get_language(string) if word not in self.key
        )
        # Беру с конца словарь букв, как в примере, потом добавляю слово, а потом уже оставшиеся буквы
        alpha_new: str = tmp[-self._step :] + self.key + tmp[: -self._step]
        return string.translate(str.maketrans(alpha_new, self._get_language(string)))
