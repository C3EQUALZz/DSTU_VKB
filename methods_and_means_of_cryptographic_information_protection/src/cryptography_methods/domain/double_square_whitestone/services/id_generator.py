from abc import abstractmethod
from typing import Protocol

from cryptography_methods.domain.double_square_whitestone.values.table_id import WhiteStoneTableID


class DoubleTableWhitestoneIdGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> WhiteStoneTableID:
        ...
