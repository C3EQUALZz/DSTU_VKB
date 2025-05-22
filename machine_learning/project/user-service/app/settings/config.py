import multiprocessing
from abc import ABC
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class CacheSettings(CommonSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT_NETWORK")
    password: str = Field(alias="REDIS_PASSWORD")

    @property
    def url(self) -> RedisDsn:
        return RedisDsn(f"redis://:{self.password}@{self.host}:{self.port}")


class AuthSettings(CommonSettings):
    private_key: str = Field(alias="PRIVATE_KEY")
    public_key: str = Field(alias="PUBLIC_KEY")
    algorithm: str = Field(default="RS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=5, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(default=10, alias="REFRESH_TOKEN_EXPIRE_MINUTES")


class ServerSettings(CommonSettings):
    multiprocess_dir: Optional[Path] = Field(alias="PROMETHEUS_MULTIPROC_DIR", default=None)
    workers: int = Field(alias="SERVER_WORKERS", default=multiprocessing.cpu_count() * 2 + 1)
    max_requests: int = Field(alias="SERVER_MAX_REQUESTS", default=1000)
    max_jitter: int = Field(alias="SERVER_MAX_JITTER", default=50)
    bind: str = Field(alias="SERVER_BIND")
    timeout: int = Field(alias="SERVER_TIMEOUT")
    worker_class: str = Field(alias="SERVER_WORKER_CLASS")
    log_level: str = Field(alias="SERVER_LOG_LEVEL")
    log_file: str = Field(alias="SERVER_LOG_FILE")
    allowed_host: str = Field(alias="ALLOWED_HOST")


class CORSSettings(CommonSettings):
    allow_origins: list[str] = Field(alias="CORS_ALLOW_ORIGINS")
    allow_headers: list[str] = Field(alias="CORS_ALLOW_HEADERS")
    allow_credentials: bool = Field(alias="CORS_ALLOW_CREDENTIALS")
    allow_methods: list[str] = Field(alias="CORS_ALLOW_METHODS")


class BrokerSettings(CommonSettings):
    host: str = Field(alias="BROKER_HOST")
    port: int = Field(alias="BROKER_PORT_NETWORK")

    user_created_topic: str = Field(default="user-created", alias="BROKER_USER_CREATED_TOPIC")
    user_updated_topic: str = Field(default="user-updated", alias="BROKER_USER_UPDATED_TOPIC")
    user_deleted_topic: str = Field(default="user-deleted", alias="BROKER_USER_DELETED_TOPIC")

    user_create_topic: str = Field(default="user-create", alias="BROKER_USER_CREATE_TOPIC")
    user_update_topic: str = Field(default="user-update", alias="BROKER_USER_UPDATE_TOPIC")
    user_delete_topic: str = Field(default="user-delete", alias="BROKER_USER_DELETE_TOPIC")

    user_telegram_id_from_start_bot_topic: str = Field(default="user-telegram-start",
                                                       alias="USER_TELEGRAM_ID_FROM_START_BOT")
    user_telegram_id_from_start_bot_group_id: str = Field(default="user-telegram-start-group",
                                                          alias="USER_TELEGRAM_ID_FROM_START_BOT_GROUP")

    user_successfully_linked_telegram_topic: str = Field(default="user-telegram-link-success",
                                                         alias="USER_SUCCESSFULLY_LINK_TOPIC")
    user_failed_link_telegram_topic: str = Field(default="user-telegram-link-failed", alias="USER_FAILED_LINK_TOPIC")

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class TelegramSettings(CommonSettings):
    url: str = Field(alias="TELEGRAM_URL")


class Settings(CommonSettings):
    """
    Класс настроек, которым в дальнейшем будет оперировать приложение.
    """

    database: DatabaseSettings = DatabaseSettings()
    alchemy_settings: SQLAlchemySettings = SQLAlchemySettings()
    broker: BrokerSettings = BrokerSettings()
    cache: CacheSettings = CacheSettings()
    auth: AuthSettings = AuthSettings()
    server: ServerSettings = ServerSettings()
    cors: CORSSettings = CORSSettings()
    telegram: TelegramSettings = TelegramSettings()
    project_dir: Path = Path(__file__).parent.parent.parent.parent


@lru_cache(1)
def get_settings() -> Settings:
    return Settings()
