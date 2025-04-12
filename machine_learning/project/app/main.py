import asyncio
import contextlib
from pathlib import Path
from typing import TYPE_CHECKING

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dishka.integrations.aiogram import setup_dishka

from app.application.telegram.handlers.image import router as image_router
from app.application.telegram.handlers.menu import router as menu_router
from app.application.telegram.handlers.text import router as text_router
from app.logic.container import get_container
from app.settings.config import (
    Settings,
    get_settings,
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

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path=Path(__file__).resolve().parent / "application" / "telegram" / "locales" / "{locale}" / "LC_MESSAGES",
            default_locale="ru",
        )
    )

    i18n_middleware.setup(dispatcher=dp)

    dp.include_router(text_router)
    dp.include_router(menu_router)
    dp.include_router(image_router)

    setup_dishka(container=container, router=dp, auto_inject=True)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
