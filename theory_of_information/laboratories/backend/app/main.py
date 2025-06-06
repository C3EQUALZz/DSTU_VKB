from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.application.api.second_semester.first_laboratory.handlers import \
    router as second_semester_first_laboratory_router
from app.application.api.second_semester.second_laboratory.handlers import \
    router as second_semester_second_laboratory_router
from app.application.api.second_semester.third_laboratory.handlers import \
    router as second_semester_third_laboratory_router
from app.application.api.second_semester.fourth_laboratory.handlers import \
    router as second_semester_fourth_laboratory_router

from app.logic.container import container
from app.settings.logger.config import setup_logging
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield

    await app.state.dishka_container.close()  # type: ignore


def create_app() -> FastAPI:
    app = FastAPI(
        title="Theory of information",
        description="Backend API written with FastAPI for laboratories",
        root_path="/api",
        docs_url="/docs",
        debug=True,
        lifespan=lifespan,
    )

    setup_logging()
    setup_dishka(container=container, app=app)
    app.include_router(second_semester_first_laboratory_router)
    app.include_router(second_semester_second_laboratory_router)
    app.include_router(second_semester_third_laboratory_router)
    app.include_router(second_semester_fourth_laboratory_router)

    return app
