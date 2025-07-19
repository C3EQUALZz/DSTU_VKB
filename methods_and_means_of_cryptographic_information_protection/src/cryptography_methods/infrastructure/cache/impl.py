import logging
import pickle
import zlib
from typing import Any, Final

from redis.asyncio import Redis
from typing_extensions import override

from cryptography_methods.infrastructure.cache.base import CacheStore, KeyWithPrefix, Prefix

logger: Final[logging.Logger] = logging.getLogger(__name__)


class RedisCacheStore(CacheStore):
    def __init__(self, redis: Redis) -> None:
        self._redis: Final[Redis] = redis

    @override
    async def set(
            self,
            key: KeyWithPrefix,
            value: Any,
            ttl: int = 30,
    ) -> None:
        full_key: str = self.__build_full_key(key)
        serialized: bytes = pickle.dumps(value)
        compressed: bytes = zlib.compress(serialized)

        logger.debug("Caching data with key: %s and ttl: %s", full_key, ttl)

        await self._redis.setex(name=full_key, value=compressed, time=ttl)

    @override
    async def get(self, key: KeyWithPrefix, default: Any | None = None) -> Any:
        full_key: str = self.__build_full_key(key)
        serialized: Any = await self._redis.get(full_key)

        if serialized is None:
            return default

        try:
            deserialized: Any = pickle.loads(serialized)
            decompressed: Any = zlib.decompress(deserialized)
            logger.debug("Returning key")
        except pickle.UnpicklingError:
            logger.exception("Failed to unpickle %s, returning default value", full_key)
            return default
        except zlib.error:
            logger.exception("Failed to uncompress %s, returning default value", full_key)
            return default
        else:
            return decompressed

    @override
    async def delete(self, key_with_prefix: KeyWithPrefix) -> None:
        full_key: str = self.__build_full_key(key_with_prefix)
        logger.debug(f"Deleting data with key: {full_key}")
        await self._redis.delete(full_key)

    @override
    async def clear_by_prefix(self, prefix: Prefix) -> None:
        """Очистить все ключи с указанным префиксом"""
        pattern: str = f"{prefix.value}:*"

        keys: list[str] = []
        async for key in self._redis.scan_iter(match=pattern):
            keys.append(key)

        if not keys:
            return

        batch_size: Final[int] = 5000

        # Making batches to reduce server load

        batches: list[list[str]] = [keys[i: i + batch_size] for i in range(0, len(keys), batch_size)]

        for batch in batches:
            async with self._redis.pipeline(transaction=False) as pipe:
                for key in batch:
                    await pipe.delete(key)
                await pipe.execute()

        keys.clear()
        batches.clear()

    @override
    async def exists(self, key: KeyWithPrefix) -> bool:
        """Проверить существование ключа"""
        full_key: str = self.__build_full_key(key)
        logger.debug(f"Checking existence of {full_key}")
        return bool(await self._redis.exists(full_key))

    @staticmethod
    def __build_full_key(key: KeyWithPrefix) -> str:
        """Строит полный ключ в формате 'prefix:key'"""
        if key.prefix is None:
            return f"{key.key.value}"
        return f"{key.prefix.value}:{key.key.value}"
