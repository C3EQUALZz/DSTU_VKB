from abc import ABC
from typing import Final

from redis.asyncio import Redis

from app.infrastructure.repositories.cache.base import BaseCacheRepository


class BaseRedisCacheRepository(BaseCacheRepository, ABC):
    def __init__(self, redis_client: Redis, default_ttl: int = 86400) -> None:
        self._cache: Final[Redis] = redis_client
        self._default_ttl: Final[int] = default_ttl
