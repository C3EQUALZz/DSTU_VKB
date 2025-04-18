from abc import ABC
from functools import lru_cache
from pathlib import Path

from pydantic import Field, RedisDsn, field_validator
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


class DatabaseSettings(CommonSettings):
    """
    Here you provide settings from .env to connect to database.
    Some params are optional because database such as sqlite doesn't need them.
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
    SQLAlchemy settings.
    For more info about this settings see the documentation of sqlalchemy.
    """

    pool_pre_ping: bool = Field(alias="DATABASE_POOL_PRE_PING")
    pool_recycle: int = Field(alias="DATABASE_POOL_RECYCLE")
    echo: bool = Field(alias="DATABASE_ECHO")
    auto_flush: bool = Field(alias="DATABASE_AUTO_FLUSH")
    expire_on_commit: bool = Field(alias="DATABASE_EXPIRE_ON_COMMIT")


class TelegramSettings(CommonSettings):
    """
    Telegram settings. Here you provide settings from .env to connect to telegram.
    """

    token: str = Field(alias="TELEGRAM_TOKEN")


class OpenAISettings(CommonSettings):
    base_url: str = Field(alias="OPENAI_BASE_URL")
    api_key: str = Field(alias="OPENAI_API_KEY")
    default_model: str = Field(alias="OPENAI_DEFAULT_MODEL", default="deepseek/deepseek-chat")


class RedisSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class ModelsSettings(CommonSettings):
    path_to_colorization_model: Path = Field(alias="PATH_TO_COLORIZATION_MODEL")

    @field_validator("path_to_colorization_model", mode="before")
    def validating_path_to_colorization_model(cls, v: str) -> Path:
        converted_to_path: Path = Path.cwd().parent.parent / Path(v)

        if not converted_to_path.exists():
            raise ValueError(f"Path {v} doesn't exists")

        return converted_to_path


class Settings(CommonSettings):
    """
    Settings class which encapsulates logic of settings from other classes.
    In application, you must use this class.
    """

    database: DatabaseSettings = DatabaseSettings()
    alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()
    telegram: TelegramSettings = TelegramSettings()
    openai: OpenAISettings = OpenAISettings()
    cache: RedisSettings = RedisSettings()
    models: ModelsSettings = ModelsSettings()


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
