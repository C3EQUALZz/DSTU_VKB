from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_language.theory_of_information.models.second_laboratory import TokenLZ77
    from python_language.theory_of_information.models.second_laboratory import TokenLZ78


class Compressor(ABC):
    @abstractmethod
    def compress(self, text: str) -> "list[TokenLZ77] | list[TokenLZ78]":
        raise NotImplementedError

    @abstractmethod
    def decompress(self, tokens: "list[TokenLZ77] | list[TokenLZ78]") -> str:
        raise NotImplementedError
