from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from redis.asyncio import (
    ConnectionPool,
    Redis,
)

from app.application.api.auth import auth_router
from app.application.api.scores import score_router
from app.application.api.users import user_router
from app.application.middlewares.client_cache import ClientCacheMiddleware
from app.core.utils.cache import cache
from app.logic.container import container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    cache.pool = await container.get(ConnectionPool)
    cache.client = await container.get(Redis)

    yield

    await cache.pool.aclose()
    await app.state.dishka_container.close()  # type: ignore


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend for pacman game",
        description="Backend API written with FastAPI for game purposes",
        root_path="/api",
        debug=True,
        lifespan=lifespan,
    )

    setup_dishka(container=container, app=app)

    app.add_middleware(ClientCacheMiddleware, max_age=60) # type: ignore

    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(score_router)

    return app
