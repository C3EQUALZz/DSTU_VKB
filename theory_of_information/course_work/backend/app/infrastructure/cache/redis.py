import json
from typing import Any, Optional

from redis.asyncio import Redis

from app.infrastructure.cache.base import BaseCache


class RedisCache(BaseCache):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self, key: str) -> Optional[Any]:
        data = await self._redis.get(key)
        if data is None:
            return None
        return json.loads(data)

    async def set(self, key: str, value: Any, expire: int = 60) -> None:
        val = json.dumps(value)
        await self._redis.set(key, val, ex=expire)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self._redis.exists(key) > 0

    async def close(self) -> None:
        await self._redis.connection_pool.aclose()
