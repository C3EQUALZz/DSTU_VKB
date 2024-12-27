from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.application.api.users import user_router
from app.application.api.auth import auth_router
from app.logic.container import container
from dishka.integrations.fastapi import setup_dishka


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend for pacman game",
        description="Backend API written with FastAPI for game purposes",
        root_path="/api",
        debug=True,
        lifespan=lifespan,
    )

    setup_dishka(container=container, app=app)

    app.include_router(user_router)
    app.include_router(auth_router)

    return app
