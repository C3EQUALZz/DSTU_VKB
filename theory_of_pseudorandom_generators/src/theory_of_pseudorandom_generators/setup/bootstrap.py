import logging
import sys
from types import TracebackType
from typing import Any

from click import Group

from theory_of_pseudorandom_generators.presentation.cli.fibonacci_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    fibonacci_generator_group,
)
from theory_of_pseudorandom_generators.presentation.cli.geffey_pseudorandom_number_generator_on_shift_registers_with_linear_feedback import (
    geffe_generator_group,
)
from theory_of_pseudorandom_generators.presentation.cli.linear_congruent_pseudorandom_number_generator import (
    linear_congruent_pseudorandom_number_generator_group,
)
from theory_of_pseudorandom_generators.presentation.cli.methodology_for_assessing_the_quality_of_gpsp_distribution_on_plane import (
    plane_distribution_group,
)
from theory_of_pseudorandom_generators.presentation.cli.methodology_for_assessing_the_quality_of_gpsp_evaluation_tests_checking_unlinked_series import (
    nist_tests_group,
)
from theory_of_pseudorandom_generators.presentation.cli.methodology_for_assessing_the_quality_of_gpsp_histogram_of_the_distribution_of_elements import (
    histogram_group,
)
from theory_of_pseudorandom_generators.presentation.cli.polynomial_congruent_pseudorandom_number_generator import (
    polynomial_congruent_pseudorandom_number_generator_group,
)
from theory_of_pseudorandom_generators.setup.config_logger import LoggingConfig, configure_logging


def setup_cli_routes(main_group: Group) -> None:
    main_group.add_command(fibonacci_generator_group)  # type: ignore
    main_group.add_command(geffe_generator_group)  # type: ignore
    main_group.add_command(linear_congruent_pseudorandom_number_generator_group)  # type: ignore
    main_group.add_command(plane_distribution_group)  # type: ignore
    main_group.add_command(nist_tests_group)  # type: ignore
    main_group.add_command(histogram_group)  # type: ignore
    main_group.add_command(polynomial_congruent_pseudorandom_number_generator_group)  # type: ignore


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
