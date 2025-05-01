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
from app.infrastructure.scheduler import scheduler
from app.infrastructure.brokers.base import BaseMessageBroker
from app.logic.container import get_container
from app.settings.logger.config import setup_logging
from app.application.api.v1.colorization.handlers import router as colorization_router
from app.application.api.v1.transformation.handlers import router as transformation_router

if TYPE_CHECKING:
    from dishka import AsyncContainer

logger: Final[Logger] = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = get_container()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    setup_dishka_faststream(container, FastStream(faststream_broker))

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
        root_path="/api/v1/image",
        lifespan=lifespan,
    )

    setup_logging()
    register_exception_handlers(app)

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(colorization_router)
    app.include_router(transformation_router)

    return app
