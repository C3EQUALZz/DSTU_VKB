import logging
from typing import TYPE_CHECKING

from aiogram import Dispatcher

from app.application.jobs import broker
from app.logic.container import get_container
from app.settings.logger.config import setup_logging

if TYPE_CHECKING:
    from dishka import AsyncContainer

logger = logging.getLogger(__name__)


async def on_start(dispatcher: Dispatcher) -> None:
    setup_logging()

    if not broker.is_worker_process:
        logger.info("Setting up taskiq")
        await broker.startup()


async def on_shutdown(dispatcher: Dispatcher) -> None:
    container: AsyncContainer = get_container()
    dispatcher.shutdown.register(container.close)

    if not broker.is_worker_process:
        logger.info("Shutting down taskiq")
        await broker.shutdown()
