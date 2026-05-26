"""Конфигурация structlog по объекту LoggingConfig."""

import logging
import sys

import structlog

from steganography.setup.settings import LoggingConfig


def configure_logging(config: LoggingConfig) -> None:
    """Богатое логирование с цветами в TTY, JSON в pipe или по флагу."""
    level: int = logging.getLevelName(config.level)
    logging.basicConfig(format="%(message)s", stream=sys.stderr, level=level)

    use_json: bool = config.json or not sys.stderr.isatty()
    renderer: structlog.types.Processor = (
        structlog.processors.JSONRenderer(ensure_ascii=False)
        if use_json
        else structlog.dev.ConsoleRenderer(colors=True)
    )

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(level),
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            renderer,
        ],
        cache_logger_on_first_use=True,
    )
