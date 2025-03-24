from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import clear_mappers

from app.application.api.v1.auth.handlers import router as auth_router
from app.application.api.v1.users.handlers import router as user_router
from app.application.api.v1.utils.handlers import register_exception_handlers
from app.application.utils.admin_setup import setup_admin
from app.infrastructure.adapters.alchemy.orm import start_mappers
from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.cache.base import BaseCache
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.container import container
from app.settings.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    cache: BaseCache = await container.get(BaseCache)

    await broker.start()

    # cache.pool = await container.get(ConnectionPool)
    # cache.client = await container.get(Redis)

    start_mappers()

    await setup_admin(await container.get(UsersUnitOfWork), await container.get(Settings))

    yield

    await broker.close()
    await cache.close()
    await app.state.dishka_container.close()
    clear_mappers()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Microservice backend for user service",
        description="Backend API written with FastAPI for user service",
        root_path="/api/v1",
        debug=True,
        lifespan=lifespan,
    )

    register_exception_handlers(app)
    setup_dishka_fastapi(container=container, app=app)

    app.include_router(user_router)
    app.include_router(auth_router)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                       "Access-Control-Allow-Origin",
                       "Authorization", "Cache-Control"]
    )

    return app
