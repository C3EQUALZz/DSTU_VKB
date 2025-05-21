import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Final

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI

from app.application.api.v1.users.handlers import router as users_router
from app.application.api.v1.utils.handlers import register_exception_handlers
from app.logic.container import get_container
from app.settings.configs.app import get_settings
from app.settings.logger.config import setup_logging

logger: Final[logging.Logger] = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()

    yield

    await app.state.dishka_container.close()  # type: ignore



def create_app() -> FastAPI:
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

    app.include_router(users_router)

    setup_dishka_fastapi(container=container, app=app)

    return app
