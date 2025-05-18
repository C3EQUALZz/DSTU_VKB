import contextlib
import logging
from logging import Logger
from typing import TYPE_CHECKING, AsyncGenerator, Final

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI
from faststream import FastStream
from faststream.kafka import KafkaBroker
from fastapi.middleware.cors import CORSMiddleware

from app.application.api.middlewares.metrics import MetricsMiddleware
from app.application.api.utils.handlers import register_exception_handlers
from app.application.api.v1 import router_v1
from app.application.api.metrics.handlers import router as metrics_router
from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.scheduler.base import BaseScheduler
from app.logic.container import get_container
from app.settings.configs.app import Settings, get_settings
from app.settings.logger.config import setup_logging

if TYPE_CHECKING:
    from dishka import AsyncContainer

logger: Final[Logger] = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = get_container()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    scheduler: BaseScheduler = await container.get(BaseScheduler)
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    setup_dishka_faststream(container, FastStream(faststream_broker, logger=logger), auto_inject=True)

    await broker.start()
    await scheduler.start()

    yield

    await broker.stop()
    await scheduler.stop()
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    container: AsyncContainer = get_container()
    settings: Settings = get_settings()

    app: FastAPI = FastAPI(
        title="Microservice backend for image service",
        description="Backend API written with FastAPI for image service",
        debug=True,
        root_path="/api",
        lifespan=lifespan,
    )

    setup_logging()

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.cors.allow_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )

    app.add_middleware(
        MetricsMiddleware,  # type: ignore
        container=container
    )

    register_exception_handlers(app)

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(router_v1)
    app.include_router(metrics_router)

    return app
