from abc import abstractmethod
from typing import Protocol


class IProcessor(Protocol):
    @abstractmethod
    def process(self) -> None:
        raise NotImplementedError
