import logging
import sys
from functools import lru_cache
from pathlib import Path
from types import TracebackType
from typing import Any, Final

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from taskiq import AsyncBroker, SmartRetryMiddleware, TaskiqScheduler, async_shared_broker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from compressor.infrastructure.persistence.models.telegram_users import map_telegram_user_table
from compressor.infrastructure.persistence.models.users import map_user_table
from compressor.presentation.telegram.handlers import setup_all_dialogs, setup_all_handlers
from compressor.presentation.telegram.middlewares.stale_message_middleware import StaleMessageMiddleware
from compressor.presentation.telegram.middlewares.timing_middleware import TimingMiddleware
from compressor.setup.configs.broker import RabbitMQConfig
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.logs import LoggingConfig, build_structlog_logger
from compressor.setup.configs.settings import AppConfig
from compressor.setup.configs.task_iq import TaskIQConfig
from compressor.setup.configs.telegram import TGConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def setup_configs() -> AppConfig:
    return AppConfig()


def setup_map_tables() -> None:
    map_telegram_user_table()
    map_user_table()


def setup_task_manager(
    taskiq_config: TaskIQConfig, rabbitmq_config: RabbitMQConfig, redis_config: RedisConfig
) -> AsyncBroker:
    logger.debug("Creating taskiq broker for task management....")
    broker: AsyncBroker = (
        AioPikaBroker(
            url=rabbitmq_config.uri,
            declare_exchange=taskiq_config.declare_exchange,
            declare_queues_kwargs={"durable": taskiq_config.durable_queue},
            declare_exchange_kwargs={"durable": taskiq_config.durable_exchange},
        )
        .with_middlewares(
            SmartRetryMiddleware(
                default_retry_count=taskiq_config.default_retry_count,
                default_delay=taskiq_config.default_delay,
                use_jitter=taskiq_config.use_jitter,
                use_delay_exponent=taskiq_config.use_delay_exponent,
                max_delay_exponent=taskiq_config.max_delay_exponent,
            ),
        )
        .with_result_backend(RedisAsyncResultBackend(redis_url=redis_config.worker_uri))
    )
    logger.debug("Set async shared broker")
    async_shared_broker.default_broker(broker)

    logger.debug("Returning taskiq broker")
    return broker


def setup_scheduler(broker: AsyncBroker) -> TaskiqScheduler:
    logger.debug("Creating taskiq scheduler for task management...")

    return TaskiqScheduler(
        broker=broker,
        sources=[LabelScheduleSource(broker)],
    )


def setup_telegram_bot_storage(
    telegram_bot_config: TGConfig,
    redis_config: RedisConfig,
) -> BaseStorage:
    logger.debug("Creating storage for telegram bot...")

    if telegram_bot_config.use_redis_storage:
        logger.debug("Setup redis storage for telegram bot...")

        return RedisStorage.from_url(
            url=redis_config.fsm_memory_uri,
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )

    logger.debug("Setup memory storage")
    return MemoryStorage()


def setup_telegram_bot_event_isolation(
    telegram_bot_config: TGConfig,
    redis_config: RedisConfig,
) -> BaseEventIsolation:
    logger.debug("Creating event isolation storage for telegram bot...")

    if telegram_bot_config.use_redis_event_isolation:
        logger.debug("Setup redis event isolation storage for telegram bot...")
        return RedisEventIsolation.from_url(
            url=redis_config.fsm_memory_uri,
        )

    logger.debug("Setup memory event isolation storage")
    return SimpleEventIsolation()


def setup_telegram_bot_middlewares(dp: Dispatcher, telegram_bot_config: TGConfig) -> None:
    logger.debug("Start setup middlewares for telegram bot...")

    path_to_locales: Path = Path("src") / "compressor" / "presentation" / "telegram" / "locales"
    logger.debug("Path to locales: %s", path_to_locales)

    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path=path_to_locales / "{locale}" / "LC_MESSAGES",
            default_locale=telegram_bot_config.default_locale,
            use_isolating=telegram_bot_config.use_i18n_isolation,
        )
    )

    dp.update.outer_middleware(StaleMessageMiddleware())
    dp.update.outer_middleware(TimingMiddleware())
    i18n_middleware.setup(dispatcher=dp)
    logger.debug("Finish setup middlewares for telegram bot...")


def setup_telegram_routes(dp: Dispatcher) -> None:
    logger.debug("Start setup routes for telegram bot...")
    setup_all_handlers(dp)
    setup_all_dialogs(dp)
    setup_dialogs(dp)
    logger.debug("Finish setup routes for telegram bot...")


def setup_telegram_bot_dispatcher(
    storage: BaseStorage,
    events_isolation: BaseEventIsolation,
) -> Dispatcher:
    logger.debug("Creating dispatcher for telegram bot...")

    dp: Dispatcher = Dispatcher(
        events_isolation=events_isolation,
        storage=storage,
    )

    logger.debug("Configured dispatcher")

    return dp


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
