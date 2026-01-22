import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Final, Any

from click import Group

from vulnfinder.setup.configs.app_config import ApplicationConfig
from vulnfinder.setup.configs.logging import LoggingConfig, configure_logging
from vulnfinder.presentation.cli import analysis_group, knowledge_base_group

logger: Final[logging.Logger] = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def setup_configs() -> ApplicationConfig:
    return ApplicationConfig()


def setup_cli_routes(main_group: Group) -> None:
    main_group.add_command(analysis_group)  # type: ignore[arg-type]
    main_group.add_command(knowledge_base_group)  # type: ignore[arg-type]


def setup_logging(logger_config: LoggingConfig) -> None:
    configure_logging(logger_config)

    root_logger: logging.Logger = logging.getLogger()

    if logger_config.level == "DEBUG":
        sys.excepthook = global_exception_handler_with_traceback
    else:
        sys.excepthook = global_exception_handler_without_traceback

    root_logger.info("Logger configured")


def global_exception_handler_with_traceback(
        exc_type: type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
) -> Any:  # noqa: ANN401
    root_logger: logging.Logger = logging.getLogger()
    root_logger.exception("Error", exc_info=(exc_type, value, traceback))


def global_exception_handler_without_traceback(
        exc_type: type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
) -> Any:  # noqa: ANN401
    root_logger: logging.Logger = logging.getLogger()
    root_logger.error("Error: %s %s", exc_type.__name__, value)
