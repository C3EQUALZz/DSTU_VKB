from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...


CT = TypeVar('CT', bound=Comparable)
