import os
from pathlib import Path
from typing import Literal, Final

from pydantic import BaseModel, Field

PATH_TO_RESOURCES: Final[Path] = Path(__file__).parent.parent.parent.parent / "resources"
EXAMPLE_SIMPLE_PERMUTATION_PATH: Final[Path] = PATH_TO_RESOURCES / "simple_data_permutation" / "1.png"


class LoggingConfig(BaseModel):
    render_json_logs: bool = Field(
        default=False,
        alias="RENDER_JSON_LOGS",
        validate_default=True,
        description="Whether or not to render JSON logs.",
    )
    path: Path | None = Field(
        default=None,
        alias="PATH_TO_SAVE_LOGS",
        validate_default=True,
        description="Path to save JSON logs.",
    )
    level: Literal["DEBUG", "INFO", "ERROR", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="DEBUG",
        alias="LOG_LEVEL",
        validate_default=True,
        description="Logging level.",
    )


class I18NConfig(BaseModel):
    path: Path = Path(__file__).parent / "presentation" / "bot" / "locales"
    default_locale: Final[str] = "ru"


class TelegramConfig(BaseModel):
    token: str = Field(
        ...,
        alias="TELEGRAM_TOKEN",
        description="Telegram bot token.",
    )
    use_fsm_redis_storage: bool = Field(
        default=False,
        alias="USE_FSM_REDIS_STORAGE",
        validate_default=True,
        description="Whether or not to use Redis storage.",
    )
    use_redis_event_isolation: bool = Field(
        default=False,
        alias="USE_REDIS_EVENT_ISOLATION",
        validate_default=True,
        description="Whether or not to use Redis event isolation.",
    )


class RedisConfig(BaseModel):
    host: str = Field(
        alias="REDIS_HOST",
        default="localhost",
        description="Redis host",
        validate_default=True
    )
    port: int = Field(
        alias="REDIS_PORT",
        default=6379,
        description="Redis port",
        validate_default=True
    )
    user: str = Field(
        alias="REDIS_USER",
        default="root",
        description="Redis user",
        validate_default=True
    )
    password: str = Field(
        alias="REDIS_PASSWORD",
        default="<PASSWORD>",
        description="Redis password",
        validate_default=True
    )
    default_cache_db: int = Field(
        alias="DEFAULT_CACHE_REDIS_DB",
        default=0,
        description="Redis db for caching events",
        validate_default=True
    )
    aiogram_fsm_cache_db: int = Field(
        alias="AIOGRAM_FSM_CACHE_DB",
        default=1,
        description="Redis db for aiogram fsm",
        validate_default=True
    )
    aiogram_event_isolation_cache_db: int = Field(
        alias="AIOGRAM_EVENT_ISOLATION_CACHE_DB",
        default=2,
        description="Redis db for aiogram events",
        validate_default=True
    )

    max_connections: int = Field(
        alias="REDIS_MAX_CONNECTIONS",
        default=20,
        description="Redis max connections",
        validate_default=True
    )

    @property
    def url(self) -> str:
        return f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.default_cache_db}"

    @property
    def aiogram_fsm_url(self) -> str:
        return f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.aiogram_fsm_cache_db}"

    @property
    def aiogram_event_isolation_url(self) -> str:
        return f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.aiogram_event_isolation_cache_db}"


class PostgresConfig(BaseModel):
    """Configuration container for PostgreSQL database connection settings.

    Attributes:
        user: Database username.
        password: Database password.
        host: Database server hostname or IP address.
        port: Database server port.
        db_name: Name of the database to connect to.

    Properties:
        uri: Complete PostgreSQL connection URI in psycopg format.
    """

    user: str = Field(
        alias="POSTGRES_USER",
        default="postgres",
        description="Database username to connect",
        validate_default=True,
    )
    password: str = Field(
        alias="POSTGRES_PASSWORD",
        default="postgres",
        description="Database password to connect",
        validate_default=True,
    )
    host: str = Field(
        alias="POSTGRES_HOST",
        default="localhost",
        description="Database server hostname or IP address",
        validate_default=True,
    )
    port: int = Field(
        alias="POSTGRES_PORT",
        default="5432",
        description="Database server port",
        validate_default=True,
    )
    db_name: str = Field(
        alias="POSTGRES_DB",
        default="user-service",
        description="Database name to connect",
        validate_default=True,
    )

    @property
    def uri(self) -> str:
        """Generates a PostgreSQL connection URI.

        Returns:
            str: Connection string in format:
                postgresql+psycopg://user:password@host:port/db_name

        Note:
            - Uses psycopg driver for async operations
            - Includes all authentication credentials
            - Suitable for SQLAlchemy's create_async_engine
        """
        full_url: str = "postgresql+asyncpg://"
        full_url += f"{self.user}:{self.password}"
        full_url += f"@{self.host}:{self.port}/{self.db_name}"
        return full_url


class SQLAlchemyConfig(BaseModel):
    """
    Configuration container for SQLAlchemy.

    Attributes:
        debug: Flag to enable debug output for database operations.
    """
    pool_pre_ping: bool = Field(
        alias="DB_POOL_PRE_PING",
        default=True,
        description="Enable database pool pre ping.",
        validate_default=True,
    )
    pool_recycle: int = Field(
        alias="DB_POOL_RECYCLE",
        default=3600,
        description="Count of database connection pools",
    )
    echo: bool = Field(
        alias="DB_ECHO",
        default=False,
        description="Enable database echo mode for debugging.",
        validate_default=True,
    )
    auto_flush: bool = Field(
        alias="DB_AUTO_FLUSH",
        default=False,
        description="Enable database auto flush mode",
        validate_default=True,
    )
    expire_on_commit: bool = Field(
        alias="DB_EXPIRE_ON_COMMIT",
        default=False,
        description="Enable database expire on commit mode",
        validate_default=True,
    )


class Configs(BaseModel):
    redis: RedisConfig = Field(
        default_factory=lambda: RedisConfig(**os.environ),
        description="Redis connection config",
    )
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging config",
    )
    telegram: TelegramConfig = Field(
        default_factory=lambda: TelegramConfig(**os.environ),
        description="Telegram settings",
    )
    i18n_config: I18NConfig = Field(
        default_factory=lambda: I18NConfig(**os.environ),
        description="I18N settings",
    )
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig(**os.environ),
        description="Postgres settings",
    )
    alchemy: SQLAlchemyConfig = Field(
        default_factory=lambda: SQLAlchemyConfig(**os.environ),
        description="SQLAlchemy settings",
    )
