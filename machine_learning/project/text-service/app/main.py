from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI
from faststream import FastStream
from faststream.kafka import KafkaBroker

from app.application.api.v1.text.handlers import router as chats_router
from app.application.api.v1.utils.handlers import register_exception_handlers
from app.infrastructure.brokers.base import BaseMessageBroker
from app.logic.container import get_container
from app.settings.logger.config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = get_container()
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    faststream_broker: KafkaBroker = await container.get(KafkaBroker)
    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)

    setup_dishka_faststream(container, FastStream(faststream_broker), auto_inject=True)

    await broker.start()

    yield

    await broker.stop()

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    container: AsyncContainer = get_container()

    app = FastAPI(
        title="Microservice backend for meeting service",
        description="Backend API written with FastAPI for meeting service",
        debug=True,
        root_path="/api/v1/text",
        lifespan=lifespan,
    )

    setup_logging()
    register_exception_handlers(app)

    app.include_router(chats_router)

    setup_dishka_fastapi(container=container, app=app)

    return app
