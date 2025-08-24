import asyncio
import logging
from typing import Final, Coroutine
from functools import partial
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka
from taskiq import AsyncBroker

from compressor.setup.bootstrap import (
    setup_logging,
    setup_telegram_bot_dispatcher,
    setup_telegram_bot_storage,
    setup_telegram_bot_event_isolation,
    setup_telegram_bot_middlewares,
    setup_telegram_routes,
    setup_task_manager
)
from compressor.setup.configs.cache import RedisConfig
from compressor.setup.configs.database import PostgresConfig, SQLAlchemyConfig
from compressor.setup.configs.settings import AppConfig
from compressor.setup.ioc import setup_providers

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def on_start(dp: Dispatcher, container: AsyncContainer, task_manager: AsyncBroker) -> None:
    if not task_manager.is_worker_process:
        logger.info("Setting up taskiq")
        await task_manager.startup()


async def on_shutdown(dp: Dispatcher, container: AsyncContainer, task_manager: AsyncBroker) -> None:
    if not task_manager.is_worker_process:
        logger.info("Shutting down taskiq")
        await task_manager.shutdown()

    dp.shutdown.register(container.close)

async def create_aiogram_app() -> None:
    config: AppConfig = AppConfig()

    setup_logging(config.logging)

    bot: Bot = Bot(
        token=config.telegram_bot.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage: BaseStorage = setup_telegram_bot_storage(
        telegram_bot_config=config.telegram_bot,
        redis_config=config.redis_config,
    )

    events_isolation: BaseEventIsolation = setup_telegram_bot_event_isolation(
        telegram_bot_config=config.telegram_bot,
        redis_config=config.redis_config,
    )

    dp: Dispatcher = setup_telegram_bot_dispatcher(
        storage=storage,
        events_isolation=events_isolation,
    )

    setup_telegram_bot_middlewares(
        dp=dp,
        telegram_bot_config=config.telegram_bot,
    )

    setup_telegram_routes(
        dp=dp
    )

    context = {
        RedisConfig: config.cache,
        PostgresConfig: config.database,
        SQLAlchemyConfig: config.alchemy,
    }

    container: AsyncContainer = make_async_container(*setup_providers(), context=context)
    setup_dishka(container=container, router=dp, auto_inject=True)

    task_manager: AsyncBroker = setup_task_manager(
        taskiq_config=config.task_manager,
        rabbitmq_config=config.broker,
        redis_config=config.cache
    )

    partial_start: partial[Coroutine[AsyncContainer, AsyncBroker, None]] = partial(
        on_start,
        container=container,
        worker=task_manager
    )

    partial_shutdown: partial[Coroutine[AsyncContainer, AsyncBroker, None]] = partial(
        on_shutdown,
        container=container,
        worker=task_manager
    )

    await dp.startup.register(partial_start)
    await dp.shutdown.register(partial_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(create_aiogram_app())
    except (KeyboardInterrupt, SystemExit):
        logger.info("The bot was turned off")
