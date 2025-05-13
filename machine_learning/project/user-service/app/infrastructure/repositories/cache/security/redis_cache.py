import logging
from typing import Optional, override, Final

from redis import RedisError

from app.infrastructure.dtos.cache.security import JTICacheDTO
from app.infrastructure.repositories.cache.redis_cache import BaseRedisCacheRepository
from app.infrastructure.repositories.cache.security.base import BaseSecurityCacheRepository

logger: Final[logging.Logger] = logging.getLogger(__name__)


class RedisCacheSecurityRepository(BaseSecurityCacheRepository, BaseRedisCacheRepository):
    @override
    async def exists(self, key: str) -> bool:
        """Checking if provided key exists in cache. """
        return await self._cache.exists(f"jti_id:{key}")

    @override
    async def set(self, dto: JTICacheDTO, ttl: int | None = None) -> bool:
        """Устанавливает значение с TTL (временем жизни)."""
        if ttl is None:
            ttl = self._default_ttl

        try:
            await self._cache.setex(name=f"jti_id:{dto.key}", value=dto.to_cache(), time=ttl)
            return True
        except RedisError as e:
            logger.error("Failed to cache event with id, error: %s", e.args[0])
            return False

    @override
    async def get(self, key: str) -> Optional[JTICacheDTO]:
        """Getting value from cache by provided key."""
        data_from_cache: bytes | None = await self._cache.get(key)

        if data_from_cache:
            return JTICacheDTO.from_cache(data_from_cache)
