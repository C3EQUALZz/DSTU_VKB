from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from faststream import FastStream
from faststream.asgi import make_ping_asgi, make_asyncapi_asgi
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import clear_mappers

from app.application.api.v1.users.handlers import router as users_router
from app.application.api.v1.utils.handlers import register_exception_handlers
from app.infrastructure.adapters.alchemy.orm import metadata, start_mappers
from app.infrastructure.brokers.base import BaseMessageBroker
from app.logic.container import get_container
from app.settings.config import Settings, get_settings
from app.settings.logger.config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings: Settings = get_settings()
    container: AsyncContainer = get_container()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)
    engine: AsyncEngine = create_async_engine(settings.database.url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_mappers()

    await broker.start()

    yield

    await broker.stop()

    await app.state.dishka_container.close()

    clear_mappers()


def create_app() -> FastAPI:
    container: AsyncContainer = get_container()

    app = FastAPI(
        title="Microservice backend for meeting service",
        description="Backend API written with FastAPI for meeting service",
        debug=True,
        root_path="/api/v1/users",
        lifespan=lifespan,
    )

    setup_logging()
    register_exception_handlers(app)

    app.include_router(users_router)

    setup_dishka_fastapi(container=container, app=app)

    return app
