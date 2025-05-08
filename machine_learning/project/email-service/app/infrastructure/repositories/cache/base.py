from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.dtos.cache.base import BaseCacheDTO


class BaseCacheRepository(ABC):
    """
    Base (interface) class for implementing a cache.
    """

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Checking if provided key exists in cache. """
        raise NotImplementedError

    @abstractmethod
    async def set(self, dto: BaseCacheDTO, ttl: int | None = None) -> bool:
        """Устанавливает значение с TTL (временем жизни)."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Optional[BaseCacheDTO]:
        """Getting value from cache by provided key."""
        raise NotImplementedError
