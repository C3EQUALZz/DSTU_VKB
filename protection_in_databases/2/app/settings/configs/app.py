from abc import ABC
from functools import lru_cache
from pathlib import Path
from typing import Final

from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict

PATH_TO_PROJECT: Final[Path] = Path(__file__).parent.parent.parent.parent


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
    ssl_cert: FilePath = PATH_TO_PROJECT / Path(Field(alias="DATABASE_SSL_CERT"))
    ssl_key: FilePath = PATH_TO_PROJECT / Path(Field(alias="DATABASE_SSL_KEY"))
    ssl_root_cert: FilePath = PATH_TO_PROJECT / Path(Field(alias="DATABASE_SSL_ROOT_CERT"))
    ssl_mode: str = "verify-full"
    ssl_min_protocol_version: str = "TLSv1.3"


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """

    database: DatabaseSettings = DatabaseSettings()
    alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
