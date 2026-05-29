"""Сборка CLI: настройка логирования и регистрация click-команд."""

import logging
import sys
from types import TracebackType
from typing import Final

from click import Group

from steganography.presentation.cli.handlers.kutter_jordan_bossen import (
    kutter_jordan_bossen_group,
)
from steganography.presentation.cli.handlers.linguistic_bit_in_string import (
    linguistic_bit_in_string_group,
)
from steganography.presentation.cli.handlers.lsb_bmp_vigenere import (
    lsb_bmp_vigenere_group,
)
from steganography.presentation.cli.handlers.lsb_hamming_bmp import (
    lsb_hamming_bmp_group,
)
from steganography.presentation.cli.handlers.text_format_decode import (
    text_format_decode_group,
)
from steganography.presentation.cli.handlers.text_format_encode import (
    text_format_encode_group,
)
from steganography.setup.logging import configure_logging
from steganography.setup.settings import LoggingConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


def setup_cli_routes(main_group: Group) -> None:
    """Регистрирует все click-группы лабораторных в корневой команде."""
    main_group.add_command(text_format_decode_group)
    main_group.add_command(text_format_encode_group)
    main_group.add_command(linguistic_bit_in_string_group)
    main_group.add_command(lsb_bmp_vigenere_group)
    main_group.add_command(lsb_hamming_bmp_group)
    main_group.add_command(kutter_jordan_bossen_group)


def setup_logging(logger_config: LoggingConfig) -> None:
    """Настраивает structlog и глобальный обработчик исключений."""
    configure_logging(logger_config)

    if logger_config.level == "DEBUG":
        sys.excepthook = _excepthook_with_traceback
    else:
        sys.excepthook = _excepthook_without_traceback

    logger.info("Logger configured")


def _excepthook_with_traceback(
    exc_type: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
) -> None:
    logging.getLogger().exception(
        "Error", exc_info=(exc_type, value, traceback),
    )


def _excepthook_without_traceback(
    exc_type: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,  # noqa: ARG001
) -> None:
    logging.getLogger().error("Error: %s %s", exc_type.__name__, value)
