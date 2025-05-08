import logging
from typing import Final
from typing import override

from redis import RedisError

from app.infrastructure.dtos.cache.events import EventCacheDTO
from app.infrastructure.repositories.cache.idempotency.events.base import BaseIdempotencyEventCacheRepository
from app.infrastructure.repositories.cache.redis_cache import BaseRedisCacheRepository

logger: Final[logging.Logger] = logging.getLogger(__name__)


class RedisIdempotencyEventCacheRepository(BaseIdempotencyEventCacheRepository, BaseRedisCacheRepository):
    @override
    async def exists(self, key: str) -> bool:
        """
        Checking if object exists in
        :param key:
        :return:
        """
        return await self._cache.exists(f"event_id:{key}")

    @override
    async def set(self, dto: EventCacheDTO, ttl: int | None = None) -> bool:
        """Устанавливает значение с TTL (временем жизни)."""
        if ttl is None:
            ttl = self._default_ttl

        try:
            await self._cache.setex(name=f"event_id:{dto.key}", value=dto.to_cache(), time=ttl)
            return True
        except RedisError as e:
            logger.error("Failed to cache event with id, error: %s", e.args[0])
            return False

    @override
    async def get(self, key: str) -> EventCacheDTO | None:
        """Getting value from cache by provided key."""
        data_from_cache: bytes | None = await self._cache.get(key)

        if data_from_cache:
            return EventCacheDTO.from_cache(data_from_cache)
