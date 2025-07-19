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
        default="INFO",
        alias="LOG_LEVEL",
        validate_default=True,
        description="Logging level.",
    )


class TelegramConfig(BaseModel):
    token: str = Field(
        ...,
        alias="TELEGRAM_TOKEN",
        description="Telegram bot token.",
    )
    use_redis_storage: bool = Field(
        default=False,
        alias="USE_REDIS_STORAGE",
        validate_default=True,
        description="Whether or not to use Redis storage.",
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
