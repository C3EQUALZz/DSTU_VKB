from dataclasses import dataclass

from app.infrastructure.dtos.cache.base import BaseCacheDTO
from typing import override, Self


@dataclass(frozen=True)
class JTICacheDTO(BaseCacheDTO):
    value: str

    @override
    @property
    def key(self) -> str:
        return self.value

    @classmethod
    @override
    def from_cache(cls, data: bytes) -> Self:
        """
        Getting a DTO object from cache
        :param data: bytes from cache
        :return: DTO object
        """
        return cls(data.decode())

    @override
    def to_cache(self) -> bytes:
        """Преобразует объект в данные для сохранения в кэше."""
        return self.value.encode()
