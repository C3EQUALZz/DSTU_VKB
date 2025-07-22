from typing import Protocol
from abc import abstractmethod


class AlphabetCreationStrategy(Protocol):
    @abstractmethod
    def create(self) -> str:
        raise NotImplementedError
