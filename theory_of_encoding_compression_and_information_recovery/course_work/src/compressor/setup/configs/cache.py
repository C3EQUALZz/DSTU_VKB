from pydantic import BaseModel, Field, RedisDsn


class RedisConfig(BaseModel):
    host: str = Field(
        alias="REDIS_HOST",
        description="Redis host",
    )
    port: int = Field(
        alias="REDIS_PORT",
        description="Redis port",
    )
    user: str = Field(
        alias="REDIS_USER",
        description="Redis user",
    )
    password: str = Field(
        alias="REDIS_USER_PASSWORD",
        description="Redis password",
    )
    cache_db: int = Field(
        alias="REDIS_CACHE_DB",
        description="Redis db for caching results",
    )
    worker_db: int = Field(
        alias="REDIS_WORKER_DB",
        description="Redis db for worker results",
    )
    max_connections: int = Field(
        default=100,
        alias="REDIS_MAX_CONNECTIONS",
        description="Redis max connections",
        validate_default=True
    )

    @property
    def cache_uri(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=f"/{self.cache_db}"
            )
        )

    @property
    def worker_uri(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=f"/{self.worker_db}"
            )
        )