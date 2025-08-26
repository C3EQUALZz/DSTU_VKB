import logging
from collections.abc import Callable
from enum import Enum
from pathlib import Path

import structlog
from pydantic import BaseModel, Field
from structlog.processors import CallsiteParameter, CallsiteParameterAdder


class LoggingLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig(BaseModel):
    level: LoggingLevel = Field(
        alias="LOGGING_LEVEL",
        default=LoggingLevel.INFO,
        description="Logging level",
        validate_default=True
    )
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


ProcessorType = Callable[
    [
        structlog.types.WrappedLogger,
        str,
        structlog.types.EventDict,
    ],
    str | bytes,
]

def get_render_processor(
        render_json_logs: bool = False,
        colors: bool = True,
) -> ProcessorType:
    if render_json_logs:
        return structlog.processors.JSONRenderer()
    return structlog.dev.ConsoleRenderer(colors=colors)


def build_structlog_logger(*, cfg: LoggingConfig) -> None:
    # Mute SQLAlchemy default logger handler
    # sa_log._add_default_handler = lambda _: None  # noqa

    common_processors = (
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
        structlog.contextvars.merge_contextvars,
        structlog.processors.format_exc_info,  # print exceptions from event dict
        CallsiteParameterAdder(
            (
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ),
        ),
    )
    structlog_processors = (
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),  # convert bytes to str
        # structlog.stdlib.render_to_log_kwargs,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    )
    logging_processors = (structlog.stdlib.ProcessorFormatter.remove_processors_meta,)
    logging_console_processors = (
        *logging_processors,
        get_render_processor(render_json_logs=cfg.render_json_logs, colors=True),
    )
    logging_file_processors = (
        *logging_processors,
        get_render_processor(render_json_logs=cfg.render_json_logs, colors=False),
    )

    handler = logging.StreamHandler()
    handler.set_name("default")
    handler.setLevel(cfg.level.value)
    console_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=common_processors,  # type: ignore
        processors=logging_console_processors,
    )
    handler.setFormatter(console_formatter)

    handlers: list[logging.Handler] = [handler]
    if cfg.path:
        cfg.path.parent.mkdir(parents=True, exist_ok=True)
        log_path = cfg.path / "logs.log" if cfg.path.is_dir() else cfg.path

        file_handler = logging.FileHandler(log_path)
        file_handler.set_name("file")
        file_handler.setLevel(cfg.level.value)
        file_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=common_processors,  # type: ignore
            processors=logging_file_processors,
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    logging.basicConfig(handlers=handlers, level=cfg.level.value)
    structlog.configure(
        processors=common_processors + structlog_processors,  # type: ignore # noqa
        logger_factory=structlog.stdlib.LoggerFactory(),
        # wrapper_class=structlog.stdlib.AsyncBoundLoggerd,  # type: ignore  # noqa
        wrapper_class=structlog.stdlib.BoundLogger,  # type: ignore
        cache_logger_on_first_use=True,
    )
