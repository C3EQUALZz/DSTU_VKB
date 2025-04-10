import asyncio

from aiogram import Dispatcher, Bot
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from app.logic.container import get_container
from app.settings.config import get_settings, Settings
from app.settings.logger.config import setup_logging


async def on_start(dispatcher: Dispatcher) -> None:
    setup_logging()



async def on_shutdown(dispatcher: Dispatcher) -> None:
    container: AsyncContainer = get_container()
    dispatcher.shutdown.register(container.close)


async def main() -> None:
    settings: Settings = get_settings()
    container: AsyncContainer = get_container()
    bot: Bot = Bot(token=settings.telegram.token)

    dp: Dispatcher = Dispatcher()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)

    setup_dishka(container=container, router=dp, auto_inject=True)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
