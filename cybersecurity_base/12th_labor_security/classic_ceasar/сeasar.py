"""
Здесь логика обычного шифра Цезаря

"""
from .enums import Letters
from .exceptions import NoSupport
import re


class CaesarCipher:
    """
    Данный класс описывает логику стандартного шифра Цезаря
    Args:
        key[int] = число сдвига
    """
    def __init__(self, key: int):
        self._key: int = key

    def _encode_abc(self, text: str) -> dict[int] | NoSupport:
        """
        Метод, который распознает введенные символы по регулярным выражениям.
        Если это будет латиница, то будет сформирован словарь с английскими буквами по сдвигу
        В ином случае с русскими буквами
        Args:
            text[str] = текст, который мы хотим зашифровать, используя шифр Цезаря
        """
        abc: None | dict[int] = None
        # Если найдена хотя бы одна буква из кириллицы, то будет такой перевод
        if re.search(r"[а-яА-Я]+", text):
            # Здесь изначально берется полностью словарь с русскими буквами и срезом мы формируем второй.
            # Второй словарь с учетом нашего сдвига. {a: d, b: e, c: f} (key = 3)
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
        """
        Метод, используя готовый словарь, переводит в новую строку
        Args:
            string[str] = строка, которую ввел пользователь на ввод
        """
        return str.translate(string, self._encode_abc(string))

    def decode(self, string: str) -> str:
        """
        Метод, который из зашифрованного возвращает исходный текст.
        Тут мы разворачиваем словарь, чтобы перевести {a: d} -> {d: a}
        Args:
            string[str] = строка, которую ввел полтьзователь на ввод.
        """
        return str.translate(string, {v: k for k, v in self._encode_abc(string).items()})
