import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Any, Final

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder, BaseStorage, BaseEventIsolation
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, RedisEventIsolation
from aiogram_dialog import setup_dialogs
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from click import Group

from cryptography_methods.infrastructure.persistence.models.users import map_user_aggregate
from cryptography_methods.presentation.bot.handlers.common import router as common_router
from cryptography_methods.presentation.bot.middlewares.stale_message_middleware import StaleMessageMiddleware
from cryptography_methods.presentation.bot.middlewares.timing_middleware import TimingMiddleware
from cryptography_methods.presentation.cli.handlers.affine_system_of_ceaser_substitutions import \
    affine_system_of_ceaser_substitutions_group
from cryptography_methods.presentation.cli.handlers.ceaser_keyword import ceaser_keyword_group
from cryptography_methods.presentation.cli.handlers.simple_data_permutation import simple_data_permutation_group
from cryptography_methods.presentation.cli.handlers.ceaser_classic import ceaser_classic_group
from cryptography_methods.presentation.cli.handlers.trithemius import trithemius_group
from cryptography_methods.presentation.cli.handlers.playfair import playfair_group
from cryptography_methods.setup.logging import configure_logging
from cryptography_methods.setup.settings import Configs, LoggingConfig, TelegramConfig, RedisConfig, I18NConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def setup_configs() -> Configs:
    return Configs()


def setup_map_tables() -> None:
    map_user_aggregate()


def setup_dispatcher(
        telegram_config: TelegramConfig,
        redis_config: RedisConfig,
) -> Dispatcher:
    storage: BaseStorage
    event_isolation: BaseEventIsolation

    if telegram_config.use_fsm_redis_storage:
        logger.info("Using Redis storage for fsm states")
        storage = RedisStorage.from_url(
            url=redis_config.aiogram_fsm_url,
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
        )
    else:
        logger.debug("Using memory storage for fsm states")
        storage = MemoryStorage()

    if telegram_config.use_redis_event_isolation:
        logger.info("Using Redis event isolation")
        event_isolation = RedisEventIsolation.from_url(
            url=redis_config.aiogram_event_isolation_url,
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
        )
    else:
        logger.info("Using memory event isolation")
        event_isolation = SimpleEventIsolation()

    dp: Dispatcher = Dispatcher(
        events_isolation=event_isolation,
        storage=storage
    )

    return dp


def setup_bot_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(StaleMessageMiddleware())
    dp.update.middleware(TimingMiddleware())
    logger.info("Configured all middlewares for bot")


def setup_bot_i18n(dp: Dispatcher, i18n_config: I18NConfig) -> None:
    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path=i18n_config.path,
            default_locale=i18n_config.default_locale,
        )
    )

    i18n_middleware.setup(dp)
    logger.info("Configured i18n for bot")


def setup_bot_routes(dp: Dispatcher) -> None:
    setup_dialogs(dp)
    dp.include_router(common_router)


def setup_cli_routes(main_group: Group) -> None:
    main_group.add_command(simple_data_permutation_group)  # type: ignore
    main_group.add_command(ceaser_classic_group) # type: ignore
    main_group.add_command(affine_system_of_ceaser_substitutions_group) # type: ignore
    main_group.add_command(ceaser_keyword_group) # type: ignore
    main_group.add_command(trithemius_group) # type: ignore
    main_group.add_command(playfair_group) # type: ignore


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
