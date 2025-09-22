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


class TelegramConfig(BaseModel):
    token: str = Field(
        ...,
        alias="TELEGRAM_TOKEN",
        description="Telegram bot token.",
    )


class Configs(BaseModel):
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(**os.environ),
        description="Logging config",
    )
    telegram: TelegramConfig = Field(
        default_factory=lambda: TelegramConfig(**os.environ),
        description="Telegram settings",
    )