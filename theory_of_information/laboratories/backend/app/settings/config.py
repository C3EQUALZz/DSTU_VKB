from abc import ABC
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
    Класс, от которого каждая настройка должна наследоваться.
    Написано с той целью, чтобы не было дублирования кода по настройке model_config.
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://{self.host}:{self.port}/{self.password}")


class Settings(CommonSettings):
    cache: RedisSettings = RedisSettings()
