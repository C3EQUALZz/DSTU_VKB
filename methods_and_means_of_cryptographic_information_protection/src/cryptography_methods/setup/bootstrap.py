import logging
import sys
from functools import lru_cache
from types import TracebackType
from typing import Any, Final

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder, BaseStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from cryptography_methods.presentation.bot.middlewares.stale_message_middleware import StaleMessageMiddleware
from cryptography_methods.setup.logging import configure_logging
from cryptography_methods.setup.settings import Configs, LoggingConfig, TelegramConfig, RedisConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def setup_configs() -> Configs:
    return Configs()


def setup_dispatcher(
        telegram_config: TelegramConfig,
        redis_config: RedisConfig,
) -> Dispatcher:
    if telegram_config.use_redis_storage:
        logger.debug("Using Redis storage")
        storage: BaseStorage = RedisStorage.from_url(
            url=redis_config.aiogram_fsm_url,
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
        )
    else:
        logger.debug("Using memory storage")
        storage: BaseStorage = MemoryStorage()

    dp: Dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
        storage=storage
    )

    return dp


def setup_bot_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(StaleMessageMiddleware())



def setup_bot_routes(dp: Dispatcher) -> None:
    ...


def setup_logging(logger_config: LoggingConfig) -> None:
    configure_logging(logger_config)

    root_logger: logging.Logger = logging.getLogger()
    root_logger.info("Logger configured")
    sys.excepthook = global_exception_handler


def global_exception_handler(
        exc_type: type[BaseException],
        value: BaseException,
        traceback: TracebackType | None,
) -> Any:  # noqa: ANN401
    root_logger: logging.Logger = logging.getLogger()
    root_logger.exception("Error", exc_info=(exc_type, value, traceback))
