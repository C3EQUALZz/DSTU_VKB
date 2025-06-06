from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import (
    Field,
    RedisDsn, SecretStr, EmailStr,
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


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    user_registered_topic: str = Field(
        default="user-registered-topic",
        alias="BROKER_USER_REGISTERED_TOPIC"
    )

    user_registered_group: str = Field(
        default="user-registered-group",
        alias="BROKER_USER_REGISTERED_GROUP"
    )

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class MailSettings(CommonSettings):
    user_name: str = Field(alias="MAIL_USERNAME")
    password: SecretStr = Field(alias="MAIL_PASSWORD")
    port: int = Field(alias="MAIL_PORT")
    server: str = Field(alias="MAIL_SERVER")
    start_tls: bool = Field(alias="MAIL_STARTTLS")
    ssl_tls: bool = Field(alias="MAIL_SSL_TLS")
    mail_from: EmailStr = Field(alias="MAIL_FROM")
    template_folder: Path = Path(__file__).parent.parent.parent.parent / 'templates',


class Settings(CommonSettings):
    """
    Settings class which encapsulates logic of settings from other classes.
    In application, you must use this class.
    """

    cache: RedisSettings = RedisSettings()
    broker: BrokerSettings = BrokerSettings()
    mail: MailSettings = MailSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
