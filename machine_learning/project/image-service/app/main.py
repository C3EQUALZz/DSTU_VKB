import contextlib
import logging
import sentry_sdk
from logging import Logger
from typing import TYPE_CHECKING, AsyncGenerator, Final

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI
from faststream import FastStream
from faststream.asgi import make_ping_asgi, make_asyncapi_asgi
from faststream.kafka import KafkaBroker
from fastapi.middleware.cors import CORSMiddleware

from app.application.api.middlewares.metrics import HTTPLatencyMetricsMiddleware
from app.application.api.utils.handlers import register_exception_handlers
from app.application.api import router as api_router
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
    faststream_app: FastStream = FastStream(faststream_broker, logger=logger)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    setup_dishka_faststream(container, faststream_app, auto_inject=True)

    app.mount("/health", make_ping_asgi(faststream_broker, timeout=5.0))
    app.mount("/asyncapi", make_asyncapi_asgi(faststream_app))

    await broker.start()
    await scheduler.start()

    yield

    await broker.stop()
    await scheduler.stop()
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    container: AsyncContainer = get_container()
    settings: Settings = get_settings()

    # sentry_sdk.init(
    #     dsn=settings.sentry.dsn,
    #     # Add data like request headers and IP for users,
    #     # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    #     send_default_pii=settings.sentry.send_default_pii,
    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for tracing.
    #     traces_sample_rate=settings.sentry.traces_sample_rate,
    #     # Set profile_session_sample_rate to 1.0 to profile 100%
    #     # of profile sessions.
    #     profile_session_sample_rate=settings.sentry.profile_session_sample_rate,
    #     # Set profile_lifecycle to "trace" to automatically
    #     # run the profiler on when there is an active transaction
    #     profile_lifecycle=settings.sentry.profile_lifecycle,
    # )

    app: FastAPI = FastAPI(
        title="Microservice backend for image service",
        description="Backend API written with FastAPI for image service",
        debug=True,
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
        HTTPLatencyMetricsMiddleware,  # type: ignore
        container=container
    )

    register_exception_handlers(app)

    setup_dishka_fastapi(container=container, app=app)

    app.include_router(api_router)
    app.include_router(metrics_router)

    return app
