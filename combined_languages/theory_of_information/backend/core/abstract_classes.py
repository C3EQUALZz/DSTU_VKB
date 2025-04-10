from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory import (
        TokenLZ77, TokenLZ78)


class Compressor(ABC):
    @abstractmethod
    def compress(self, text: str) -> "list[TokenLZ77] | list[TokenLZ78] | bytes":
        raise NotImplementedError

    @abstractmethod
    def decompress(self, tokens: "list[TokenLZ77] | list[TokenLZ78]") -> str:
        raise NotImplementedError


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
