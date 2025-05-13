from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.dtos.cache.security import JTICacheDTO
from app.infrastructure.repositories.cache.base import BaseCacheRepository


class BaseSecurityCacheRepository(BaseCacheRepository, ABC):
    @abstractmethod
    async def set(self, dto: JTICacheDTO, ttl: int | None = None) -> bool:
        """Устанавливает значение с TTL (временем жизни)."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Optional[JTICacheDTO]:
        """Getting value from cache by provided key."""
        raise NotImplementedError
