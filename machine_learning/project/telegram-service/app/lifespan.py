import logging
from typing import TYPE_CHECKING

from aiogram import Dispatcher

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.scheduler import scheduler
from app.logic.container import get_container
from app.settings.logger.config import setup_logging


if TYPE_CHECKING:
    from dishka import AsyncContainer

logger = logging.getLogger(__name__)


async def on_start(dispatcher: Dispatcher) -> None:
    container: AsyncContainer = get_container()
    setup_logging()

    broker = await container.get(BaseMessageBroker)

    await broker.start()

    if not scheduler.is_worker_process:
        logger.info("Setting up taskiq")
        await scheduler.startup()


async def on_shutdown(dispatcher: Dispatcher) -> None:
    container: AsyncContainer = get_container()
    broker = await container.get(BaseMessageBroker)

    await broker.stop()

    dispatcher.shutdown.register(container.close)

    if not scheduler.is_worker_process:
        logger.info("Shutting down taskiq")
        await scheduler.shutdown()
