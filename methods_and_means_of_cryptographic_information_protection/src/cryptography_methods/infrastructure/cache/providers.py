from collections.abc import AsyncIterator

from redis import ConnectionPool
from redis.asyncio import Redis

from cryptography_methods.setup.settings import RedisConfig


async def get_redis_pool(redis_config: RedisConfig) -> AsyncIterator[ConnectionPool]:
    connection_pool: ConnectionPool = ConnectionPool.from_url(
        url=redis_config.url,
        max_connections=redis_config.max_connections,
        decode_responses=False,
    )
    yield connection_pool
    connection_pool.close()


async def get_redis(connection_pool: ConnectionPool) -> AsyncIterator[Redis]:
    client: Redis = Redis.from_pool(connection_pool=connection_pool)
    yield client
    await client.close()