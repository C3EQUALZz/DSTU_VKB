from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class BaseCacheDTO(ABC):
    @classmethod
    @abstractmethod
    def from_cache(cls, data: bytes) -> Self:
        """Преобразует данные из кэша в объект."""
        raise NotImplementedError

    @abstractmethod
    def to_cache(self) -> bytes:
        """Преобразует объект в данные для сохранения в кэше."""
        raise NotImplementedError

    @abstractmethod
    @property
    def key(self) -> str:
        raise NotImplementedError
