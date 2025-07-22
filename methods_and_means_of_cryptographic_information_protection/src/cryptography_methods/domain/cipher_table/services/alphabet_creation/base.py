from typing import Protocol
from abc import abstractmethod


class AlphabetCreationStrategy(Protocol):
    @abstractmethod
    def create(self, uppercase_symbols: bool = False) -> str:
        raise NotImplementedError
