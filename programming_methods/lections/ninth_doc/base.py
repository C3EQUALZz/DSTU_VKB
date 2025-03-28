from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Tuple, Any

K = TypeVar('K')
V = TypeVar('V')


class BaseDict(ABC, Generic[K, V]):
    def __init__(self, initial_size: int = 8, load_factor: float = 0.75) -> None:
        self.size = initial_size
        self.load_factor = load_factor
        self._count = 0

    def _hash(self, key: K) -> int:
        return hash(key) % self.size

    @abstractmethod
    def __setitem__(self, key: K, value: V) -> None: ...

    @abstractmethod
    def __getitem__(self, key: K) -> V: ...

    @abstractmethod
    def __delitem__(self, key: K) -> None: ...

    @abstractmethod
    def __contains__(self, key: K) -> bool: ...

    @abstractmethod
    def _resize(self, new_size: int) -> None: ...

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={self.size}, items={len(self)})"
