from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.api.users.handlers import router as user_router
from app.logic.container import container
from dishka.integrations.fastapi import setup_dishka

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend for pacman game",
        description="Backend API written with FastAPI for game purposes",
        root_path="/api",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(user_router)

    setup_dishka(container=container, app=app)

    return app
