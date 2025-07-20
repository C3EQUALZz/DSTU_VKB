import asyncio
import logging
from functools import partial
from typing import Final, Any

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka as setup_aiogram_dishka

from cryptography_methods.setup.bootstrap import (
    setup_logging,
    setup_dispatcher,
    setup_bot_middlewares,
    setup_bot_i18n,
    setup_bot_routes,
    setup_map_tables
)

from cryptography_methods.setup.ioc import setup_providers
from cryptography_methods.setup.settings import (
    Configs,
    PostgresConfig,
    SQLAlchemyConfig,
    RedisConfig
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def on_start(dp: Dispatcher, container: AsyncContainer) -> None:
    setup_map_tables()


async def on_shutdown(dp: Dispatcher, container: AsyncContainer) -> None:
    dp.shutdown.register(container.close)


async def main() -> None:
    configs: Configs = Configs()
    setup_logging(logger_config=configs.logging)
    dp: Dispatcher = setup_dispatcher(telegram_config=configs.telegram, redis_config=configs.redis)
    setup_bot_middlewares(dp)
    setup_bot_i18n(dp=dp, i18n_config=configs.i18n_config)
    setup_bot_routes(dp=dp)

    bot: Bot = Bot(
        token=configs.telegram.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    context: dict[Any, Any] = {
        PostgresConfig: configs.postgres,
        SQLAlchemyConfig: configs.alchemy,
        RedisConfig: configs.redis,
    }

    container: AsyncContainer = make_async_container(
        *setup_providers(),
        context=context
    )

    dp.startup.register(partial(on_start, container=container))
    dp.shutdown.register(partial(on_shutdown, container=container))

    setup_aiogram_dishka(container=container, router=dp, auto_inject=True)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("The bot was turned off")
