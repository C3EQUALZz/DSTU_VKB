import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Any, Final

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage
from aiogram_dialog import setup_dialogs
from click import Group

from cryptography_methods.presentation.bot.handlers.atbash import setup_atbash_routers, setup_atbash_dialogs
from cryptography_methods.presentation.bot.handlers.common import router as common_router
from cryptography_methods.presentation.bot.middlewares.stale_message_middleware import StaleMessageMiddleware
from cryptography_methods.presentation.bot.middlewares.timing_middleware import TimingMiddleware
from cryptography_methods.presentation.cli.handlers.affine_system_of_ceaser_substitutions import (
    affine_system_of_ceaser_substitutions_group
)
from cryptography_methods.presentation.cli.handlers.ceaser_classic import ceaser_classic_group
from cryptography_methods.presentation.cli.handlers.ceaser_keyword import ceaser_keyword_group
from cryptography_methods.presentation.cli.handlers.double_square_whitestone import double_square_whitestone_group
from cryptography_methods.presentation.cli.handlers.linear_feedback_shift_register import linear_feedback_group
from cryptography_methods.presentation.cli.handlers.magic_table import magic_table_group
from cryptography_methods.presentation.cli.handlers.playfair import playfair_group
from cryptography_methods.presentation.cli.handlers.simple_data_permutation import simple_data_permutation_group
from cryptography_methods.presentation.cli.handlers.single_key_permutation import single_key_permutation_group
from cryptography_methods.presentation.cli.handlers.trithemius import trithemius_group
from cryptography_methods.presentation.cli.handlers.vigenere import vigenere_group
from cryptography_methods.presentation.cli.handlers.gost_28147 import gost_28147_group
from cryptography_methods.setup.logging import configure_logging
from cryptography_methods.setup.settings import Configs, LoggingConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def setup_configs() -> Configs:
    return Configs()


def setup_dispatcher() -> Dispatcher:
    storage: BaseStorage
    event_isolation: BaseEventIsolation

    logger.debug("Using memory storage for fsm states")
    storage = MemoryStorage()

    logger.info("Using memory event isolation")
    event_isolation = SimpleEventIsolation()

    dp: Dispatcher = Dispatcher(
        events_isolation=event_isolation,
        storage=storage
    )

    setup_atbash_routers(dp)
    setup_atbash_dialogs(dp)

    return dp


def setup_bot_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(StaleMessageMiddleware())
    dp.update.middleware(TimingMiddleware())
    logger.info("Configured all middlewares for bot")


def setup_bot_routes(dp: Dispatcher) -> None:
    setup_dialogs(dp)
    dp.include_router(common_router)


def setup_cli_routes(main_group: Group) -> None:
    main_group.add_command(simple_data_permutation_group)  # type: ignore
    main_group.add_command(single_key_permutation_group)  # type: ignore
    main_group.add_command(ceaser_classic_group)  # type: ignore
    main_group.add_command(affine_system_of_ceaser_substitutions_group)  # type: ignore
    main_group.add_command(ceaser_keyword_group)  # type: ignore
    main_group.add_command(trithemius_group)  # type: ignore
    main_group.add_command(playfair_group)  # type: ignore
    main_group.add_command(vigenere_group)  # type: ignore
    main_group.add_command(magic_table_group)  # type: ignore
    main_group.add_command(double_square_whitestone_group)  # type: ignore
    main_group.add_command(linear_feedback_group)  # type: ignore
    main_group.add_command(gost_28147_group)  # type: ignore


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
