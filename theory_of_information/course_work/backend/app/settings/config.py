from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import Field, RedisDsn
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


class DatabaseSettings(CommonSettings):
    """
    Настройки для подключения к базе данных.
    Здесь есть параметры Optional с той целью, потому что может использоваться sqlite.
    """

    host: str | None = Field(alias="DATABASE_HOST", default=None)
    port: int | None = Field(alias="DATABASE_PORT_NETWORK", default=None)
    user: str | None = Field(alias="DATABASE_USER", default=None)
    password: str | None = Field(alias="DATABASE_PASSWORD", default=None)
    name: str = Field(alias="DATABASE_NAME")
    dialect: str = Field(alias="DATABASE_DIALECT")
    driver: str = Field(alias="DATABASE_DRIVER")

    @property
    def url(self) -> str:
        if self.dialect == "sqlite":
            return f"{self.dialect}+{self.driver}:///{self.name}"

        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class SQLAlchemySettings(CommonSettings):
    """
    Настройки SQLAlchemy, полученные из env.
    """

    pool_pre_ping: bool = Field(alias="DATABASE_POOL_PRE_PING")
    pool_recycle: int = Field(alias="DATABASE_POOL_RECYCLE")
    echo: bool = Field(alias="DATABASE_ECHO")
    auto_flush: bool = Field(alias="DATABASE_AUTO_FLUSH")
    expire_on_commit: bool = Field(alias="DATABASE_EXPIRE_ON_COMMIT")


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class AdminSettings(CommonSettings):
    email: str = Field(alias="ADMIN_EMAIL")
    surname: str = Field(alias="ADMIN_SURNAME")
    name: str = Field(alias="ADMIN_NAME")
    patronymic: str = Field(alias="ADMIN_PATRONYMIC")
    password: str = Field(alias="ADMIN_PASSWORD")
    telegram_uri: str = Field(alias="ADMIN_TELEGRAM_URI")


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class AuthSettings(CommonSettings):
    """
    Общие настройки аутентификации
    """

    private_key: str = Field(alias="PRIVATE_KEY")
    public_key: str = Field(alias="PUBLIC_KEY")
    algorithm: str = Field(default="RS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=5, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(default=10, alias="REFRESH_TOKEN_EXPIRE_MINUTES")


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """

    database: DatabaseSettings = DatabaseSettings()
    alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()
    cache: RedisSettings = RedisSettings()
    admin: AdminSettings = AdminSettings()
    broker: BrokerSettings = BrokerSettings()
    auth: AuthSettings = AuthSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
