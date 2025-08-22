import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Any

from compressor.setup.configs.logs import build_structlog_logger, LoggingConfig
from compressor.setup.configs.settings import AppConfig


@lru_cache(maxsize=1)
def setup_configs() -> AppConfig:
    return AppConfig()


def setup_logging(logger_config: LoggingConfig) -> None:
    build_structlog_logger(cfg=logger_config)

    root_logger: logging.Logger = logging.getLogger()
    sys.excepthook = global_exception_handler_with_traceback
    root_logger.info("Logger configured")


def global_exception_handler_with_traceback(
        exc_type: type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
) -> Any:  # noqa: ANN401
    root_logger: logging.Logger = logging.getLogger()
    root_logger.exception("Error", exc_info=(exc_type, value, traceback))
