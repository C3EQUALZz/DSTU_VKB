"""Конфигурация приложения, читается из переменных окружения."""

import os
from dataclasses import dataclass
from typing import Final, Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


@dataclass(frozen=True)
class LoggingConfig:
    """Параметры структурированного логирования."""

    level: LogLevel = "INFO"
    json: bool = False


_VALID_LEVELS: Final[frozenset[str]] = frozenset(
    ("DEBUG", "INFO", "WARNING", "ERROR"),
)


def build_logging_config() -> LoggingConfig:
    raw_level: str = os.environ.get("STEGANOGRAPHY_LOG_LEVEL", "INFO").upper()
    level: LogLevel = (
        raw_level  # type: ignore[assignment]
        if raw_level in _VALID_LEVELS
        else "INFO"
    )
    json_flag: bool = os.environ.get("STEGANOGRAPHY_LOG_JSON", "0") == "1"
    return LoggingConfig(level=level, json=json_flag)
