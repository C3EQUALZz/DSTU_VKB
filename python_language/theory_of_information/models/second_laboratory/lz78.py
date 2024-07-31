from python_language.theory_of_information.core.abstract_classes import Compressor
from typing import override, Self, Iterator
from dataclasses import dataclass, astuple
from python_language.theory_of_information.core.decorators import loggable


@dataclass
class Token:
    index: int
    char: str

    def __repr__(self) -> str:
        return f"({self.index}, '{self.char}')"

    def __iter__(self) -> Iterator:
        return iter(astuple(self))

    def __eq__(self, other: Self | list | tuple) -> bool:
        """
        Магический метод, который просто проверяет на равенство, нужен больше для тестов
        """
        if isinstance(other, Token):
            return (self.index, self.char) == (other.index, other.char)

        if isinstance(other, (list, tuple)):
            return (self.index, self.char) == (other[0], other[1])

        return False


class LZ78(Compressor):

    @loggable
    @override
    def compress(self, text: str) -> list[Token]:
        """
        Compresses the input text using LZ78 algorithm.

        :param text: Input text to compress.
        :return: List of tuples where each tuple is (index, char).
        """
        compressed = []
        dictionary = {}
        current_string = ""

        for char in text:
            current_string += char
            if current_string not in dictionary:
                index = len(dictionary) + 1
                dictionary[current_string] = index
                token = Token(dictionary.get(current_string[:-1], 0), char)
                compressed.append(token)
                current_string = ""

        return compressed

    @loggable
    @override
    def decompress(self, compressed: list[Token]) -> str:
        """
        Decompresses the list of tuples back to the original text using LZ78 algorithm.

        :param compressed: List of tuples where each tuple is (index, char).
        :return: Decompressed text.
        """
        dictionary = {0: ""}
        decompressed = ""

        for token in compressed:
            entry = dictionary.get(token.index, "") + token.char
            decompressed += entry
            dictionary[len(dictionary)] = entry

        return decompressed
