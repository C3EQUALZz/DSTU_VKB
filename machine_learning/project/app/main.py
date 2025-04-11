import asyncio
import contextlib
from typing import TYPE_CHECKING

from aiogram import (
    Bot,
    Dispatcher,
)
from dishka.integrations.aiogram import setup_dishka

from app.application.telegram.message.user.text.handlers import router as user_router
from app.logic.container import get_container
from app.settings.config import (
    get_settings,
    Settings,
)
from app.settings.logger.config import setup_logging


if TYPE_CHECKING:
    from dishka import AsyncContainer


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

    dp.include_router(user_router)

    setup_dishka(container=container, router=dp, auto_inject=True)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
