from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Union

NumberType = Union[int, float, complex, Decimal]


class GCDStrategy(ABC):
    def __init__(self) -> None:
        self._iterations: int = 0

    @abstractmethod
    def compute(self, a: NumberType, b: NumberType) -> NumberType:
        raise NotImplementedError

    @property
    def iterations(self) -> int:
        return self._iterations
