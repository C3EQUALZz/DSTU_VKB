from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import (
    Field,
    RedisDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class CommonSettings(BaseSettings, ABC):
    """
    Base class for each setting. If you add new technologies, please add new class and inherit from BaseSettings.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class TelegramSettings(CommonSettings):
    """
    Telegram settings. Here you provide settings from .env to connect to telegram.
    """

    token: str = Field(alias="TELEGRAM_TOKEN")


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class HTTPXSettings(CommonSettings):
    user_microservice_url: str = Field(alias="USER_MICROSERVICE_URL")



class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    ...

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class Settings(CommonSettings):
    """
    Settings class which encapsulates logic of settings from other classes.
    In application, you must use this class.
    """

    telegram: TelegramSettings = TelegramSettings()
    cache: RedisSettings = RedisSettings()
    broker: BrokerSettings = BrokerSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
