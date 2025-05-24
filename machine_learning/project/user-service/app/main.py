import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Final

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from faststream.asgi import make_ping_asgi, make_asyncapi_asgi
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import clear_mappers
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.application.api.middlewares.metrics import HTTPLatencyMetricsMiddleware
from app.application.api.v1.auth.handlers import router as auth_router
from app.application.api.v1.users.handlers import router as users_router
from app.application.api.v1.utils.handlers import register_exception_handlers
from app.infrastructure.adapters.alchemy.orm import metadata, start_mappers
from app.infrastructure.brokers.base import BaseMessageBroker
from app.logic.container import get_container
from app.settings.config import Settings, get_settings
from app.settings.logger.config import setup_logging
from app.application.api.v1.telegram.handlers import router as telegram_router

logger: Final[logging.Logger] = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings: Settings = get_settings()
    container: AsyncContainer = get_container()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    faststream_app: FastStream = FastStream(faststream_broker, logger=logger)
    setup_dishka_faststream(container, FastStream(faststream_broker, logger=logger), auto_inject=True)

    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)

    engine: AsyncEngine = create_async_engine(settings.database.url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    app.mount("/health", make_ping_asgi(faststream_broker, timeout=5.0))
    app.mount("/asyncapi", make_asyncapi_asgi(faststream_app))

    await broker.start()

    yield

    await broker.stop()

    await app.state.dishka_container.close()

    clear_mappers()


def create_app() -> FastAPI:
    settings: Settings = get_settings()
    container: AsyncContainer = get_container()

    app = FastAPI(
        title="Microservice backend for user service",
        description="Backend API written with FastAPI for user service",
        debug=True,
        root_path="/api/v1/users",
        lifespan=lifespan,
    )

    setup_logging()
    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.cors.allow_origins,  # Разрешить все домены
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )

    app.add_middleware(
        HTTPLatencyMetricsMiddleware,  # type: ignore
        container=container
    )

    # app.add_middleware(
    #     TrustedHostMiddleware, # type: ignore
    #     allowed_hosts=settings.server.allowed_host,
    # )

    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(telegram_router)

    setup_dishka_fastapi(container=container, app=app)

    return app
