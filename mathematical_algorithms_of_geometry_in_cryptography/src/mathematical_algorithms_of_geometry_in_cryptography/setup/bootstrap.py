import logging
import sys
from types import TracebackType
from typing import Any

from click import Group

from mathematical_algorithms_of_geometry_in_cryptography.presentation.miller_rabin_test import miller_rabin_test_group
from mathematical_algorithms_of_geometry_in_cryptography.presentation.pollard_rho_test import pollard_rho_test_group
from mathematical_algorithms_of_geometry_in_cryptography.setup.config_logger import LoggingConfig, configure_logging


def setup_cli_routes(main_group: Group) -> None:
    main_group.add_command(miller_rabin_test_group) # type: ignore
    main_group.add_command(pollard_rho_test_group) # type: ignore


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
