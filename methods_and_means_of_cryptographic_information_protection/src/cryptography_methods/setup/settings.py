import os
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field


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
    db: int = Field(
        alias="REDIS_DB",
        default=0,
        description="Redis db",
        validate_default=True
    )

    @property
    def url(self) -> str:
        return f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


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
