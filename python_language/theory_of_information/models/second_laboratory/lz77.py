"""
Он использует метод “скользящего окна”. Внутри скользящего окна у нас есть:
    - буфер поиска
    - буфер прогноза
len(sliding_window) = len(search_buffer) + len(look_ahead_buffer)

LZ77 управляет словарем, который использует тройки, состоящие из:
    - Смещение в буфер поиска, это расстояние между началом фразы и
началом файла.
    - Длина совпадения, это количество символов, составляющих фразу.
    - Индикатор представлен символом, который будет закодирован следующим.

По мере анализа файла словарь динамически обновляется, чтобы отразить
содержимое и размер сжатых данных.

Полезные источники:
- https://youtu.be/zev2A2uWYsM?si=mwMDVEYJmonx9lBR
"""

from dataclasses import dataclass, astuple
from typing import Self
from python_language.theory_of_information.core.decorators import loggable


@dataclass
class Token:
    """
    Класс данных, представляющий собой триплет, называемый токеном, состоящий из длины, смещения
    и индикатора. Этот триплет используется при сжатии LZ77.
    """

    offset: int
    length: int
    indicator: str

    def __repr__(self) -> str:
        """
        Отображения для интерпретатора + для консоли
        """
        return f"({self.offset}, {self.length}, '{self.indicator}')"

    def __eq__(self, other: Self | list | tuple) -> bool:
        """
        Магический метод, который просто проверяет на равенство, нужен больше для тестов
        """
        if isinstance(other, Token):
            return (self.offset, self.length, self.indicator) == (other.offset, other.length, other.indicator)

        if isinstance(other, (list, tuple)):
            return (self.offset, self.length, self.indicator) == (other[0], other[1], other[2])

        return False

    def __iter__(self):
        return iter(astuple(self))


class LZ77:
    """
    Класс, содержащий методы сжатия и распаковки с использованием алгоритма сжатия LZ77.
    """

    @loggable
    def __init__(
            self,
            window_size: int = 13,
            lookahead_buffer_size: int = 6
    ) -> None:

        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size
        self.search_buffer_size = self.window_size - self.lookahead_buffer_size

    @loggable
    def compress(self, text: str) -> list[Token]:
        """
        Метод, который сжимает заданный текст строки.

        :param text: строка, которая должна быть сжата

        :return: the compressed text as a list of Tokens
        """

        output = []
        search_buffer = ""

        while text:
            # находим следующую кодирующую фразу,
            # то есть это триплет со смещением, длиной, индикатором (следующий символ кодировки)
            token = self._find_encoding_token(text, search_buffer)

            # обновляем буфер поиска:
            # - добавляем в него новые символы из текста
            # - проверьте, не превышает ли его размер максимальный размер буфера поиска, если да, удалите
            # самые старые элементы
            search_buffer += text[:token.length + 1]
            if len(search_buffer) > self.search_buffer_size:
                search_buffer = search_buffer[-self.search_buffer_size:]

            # обновляем текст
            text = text[token.length + 1:]

            # добавляем токен в конец
            output.append(token)

        return output

    # noinspection PyMethodMayBeStatic
    @loggable
    def decompress(self, tokens: list[Token]) -> str:
        """
        Разжимаем обратно в строку, т.е список токенов в выходную строку.

        :param tokens: Список, содержащий тройки (offset, length, char).

        :returns: "Разжатый" текст
        """

        output = ""

        for token in tokens:
            for _ in range(token.length):
                output += output[-token.offset]
            output += token.indicator

        return output

    @loggable
    def _find_encoding_token(self, text: str, search_buffer: str) -> Token:
        """
        Находит первое вхождение символа в тексте.
        """

        if not text:
            raise ValueError("We need some text to work with.")

        length, offset = 0, 0

        if not search_buffer:
            return Token(offset, length, text[length])

        for i, character in enumerate(search_buffer):
            found_offset = len(search_buffer) - i
            if character == text[0]:
                found_length = self._match_length_from_index(text, search_buffer, 0, i)
                # если найденная длина больше текущей или равна ей,
                # это означает, что ее смещение меньше: обновите смещение и длину
                if found_length >= length:
                    offset, length = found_offset, found_length

        return Token(offset, length, text[length])

    @loggable
    def _match_length_from_index(
            self,
            text: str,
            window: str,
            text_index: int,
            window_index: int
    ) -> int:
        """Вычисляем максимально возможное совпадение символов text и window из
        значений text_index в text и window_index в window.

        :param text: сам наш текст
        :param window: сама наша очередь
        :param text_index: индекс начала текста
        :param window_index: индекс символа в скользящем окне (очереди)

        :returns: The maximum match between text and window, from given indexes.
        """
        if not text or text[text_index] != window[window_index]:
            return 0
        return 1 + self._match_length_from_index(
            text,
            window + text[text_index],
            text_index + 1,
            window_index + 1
        )
