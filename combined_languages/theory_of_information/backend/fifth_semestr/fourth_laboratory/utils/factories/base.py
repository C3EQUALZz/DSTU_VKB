from abc import ABC, abstractmethod
from typing import Any


class Factory(ABC):
    @classmethod
    @abstractmethod
    def create(cls, matrix, matrix_type: str) -> Any:
        ...
