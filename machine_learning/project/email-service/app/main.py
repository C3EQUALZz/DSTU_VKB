import contextlib
import logging
from logging import Logger
from typing import TYPE_CHECKING, AsyncGenerator, Final

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI
from faststream import FastStream
from faststream.kafka import KafkaBroker

from app.application.api.utils.handlers import register_exception_handlers
from app.infrastructure.brokers.publishers.kafka.base import BaseKafkaPublisher
from app.infrastructure.scheduler import scheduler
from app.logic.container import get_container
from app.settings.logger.config import setup_logging

if TYPE_CHECKING:
    from dishka import AsyncContainer

logger: Final[Logger] = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = get_container()
    broker: BaseKafkaPublisher = await container.get(BaseKafkaPublisher)
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    setup_dishka_faststream(container, FastStream(faststream_broker, logger=logger), auto_inject=True)

    await broker.start()

    if not scheduler.is_worker_process:
        logger.info("Setting up taskiq")
        await scheduler.startup()

    yield

    await broker.stop()

    if not scheduler.is_worker_process:
        await scheduler.shutdown()

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    container: AsyncContainer = get_container()

    app: FastAPI = FastAPI(
        title="Microservice backend for image service",
        description="Backend API written with FastAPI for image service",
        debug=True,
        root_path="/api/v1/email",
        lifespan=lifespan,
    )

    setup_logging()
    register_exception_handlers(app)

    setup_dishka_fastapi(container=container, app=app)

    return app
