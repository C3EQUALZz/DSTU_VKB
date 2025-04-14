import asyncio
import contextlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dishka.integrations.aiogram import setup_dishka as setup_aiogram_dishka

from app import lifespan
from app.application.telegram.handlers.common import router as menu_router
from app.application.telegram.handlers.image import router as image_router
from app.application.telegram.handlers.text import router as text_router
from app.logic.container import get_container
from app.settings.config import get_settings

if TYPE_CHECKING:
    from dishka import AsyncContainer

logger = logging.getLogger(__name__)

bot: Bot = Bot(token=get_settings().telegram.token)
dp: Dispatcher = Dispatcher()


async def main() -> None:
    container: AsyncContainer = get_container()

    dp.startup.register(lifespan.on_start)
    dp.shutdown.register(lifespan.on_shutdown)

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

    setup_aiogram_dishka(container=container, router=dp, auto_inject=True)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
