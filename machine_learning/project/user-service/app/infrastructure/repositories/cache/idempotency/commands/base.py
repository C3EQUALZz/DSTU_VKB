from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.dtos.cache.commands import CommandCacheDTO
from app.infrastructure.repositories.cache.base import BaseCacheRepository


class BaseIdempotencyCommandCacheRepository(BaseCacheRepository, ABC):
    """
    Base (interface) class for implementing a cache.
    """

    @abstractmethod
    async def set(self, dto: CommandCacheDTO, ttl: int | None = None) -> bool:
        """Устанавливает значение с TTL (временем жизни)."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Optional[CommandCacheDTO]:
        """Getting value from cache by provided key."""
        raise NotImplementedError
