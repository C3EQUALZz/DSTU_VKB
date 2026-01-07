import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, cast, Final

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import clear_mappers

from chat_service.setup.bootstrap import (
    setup_configs,
    setup_map_tables,
    setup_http_routes,
    setup_http_middlewares,
    setup_http_exc_handlers
)
from chat_service.setup.config.asgi import ASGIConfig
from chat_service.setup.config.database import SQLAlchemyConfig, PostgresConfig
from chat_service.setup.config.openrouter import OpenRouterConfig
from chat_service.setup.config.settings import AppConfig
from chat_service.setup.ioc import setup_providers

logger: Final[logging.Logger] = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Async context manager for FastAPI application lifecycle management.

    Handles the startup and shutdown events of the FastAPI application.
    Specifically ensures proper cleanup
        of Dishka container resources on shutdown.

    Args:
        app: FastAPI application instance. Positional-only parameter.

    Yields:
        None: Indicates successful entry into the context.

    Note:
        The actual resource cleanup (Dishka container closure)
            happens after yield, during the application shutdown phase.
    """
    setup_map_tables()

    yield

    clear_mappers()
    await cast("AsyncContainer", app.state.dishka_container).close()


def create_fastapi_app() -> FastAPI:  # pragma: no cover
    """Creates and configures a FastAPI application
        instance with all dependencies.

    Performs comprehensive application setup including:
    - Configuration initialization
    - Dependency injection container setup
    - Database mapping
    - Route registration
    - Exception handlers
    - Middleware stack
    - Dishka integration

    Returns:
        FastAPI: Fully configured application instance ready for use.

    Side Effects:
        - Configures global application state
        - Initializes database mappings
        - Sets up observability tools
        - Registers all route handlers
    """
    configs: AppConfig = setup_configs()

    app: FastAPI = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        version="1.0.0",
        root_path="/api",
        debug=configs.asgi.fastapi_debug,
    )

    context = {
        ASGIConfig: configs.asgi,
        SQLAlchemyConfig: configs.alchemy,
        PostgresConfig: configs.postgres,
        OpenRouterConfig: configs.openrouter,
    }

    container: AsyncContainer = make_async_container(*setup_providers(), context=context)
    setup_http_routes(app)
    setup_http_exc_handlers(app)
    setup_http_middlewares(app, api_config=configs.asgi)
    setup_dishka(container, app)
    logger.info("App created", extra={"app_version": app.version})
    return app
