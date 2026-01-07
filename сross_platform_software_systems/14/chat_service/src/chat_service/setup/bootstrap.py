from functools import lru_cache

from fastapi import FastAPI, APIRouter

from chat_service.infrastructure.persistence.models.chat import map_chats_table, map_messages_table
from chat_service.infrastructure.persistence.models.user import map_users_table
from chat_service.presentation.http.v1.common.exception_handler import ExceptionHandler
from chat_service.presentation.http.v1.common.routes import index, healthcheck
from chat_service.presentation.http.v1.routes.chat import chat_router
from chat_service.setup.config.asgi import ASGIConfig
from chat_service.setup.config.settings import AppConfig


@lru_cache(maxsize=1)
def setup_configs() -> AppConfig:
    return AppConfig()


def setup_map_tables() -> None:
    """
    Ensures imperative SQLAlchemy mappings are initialized at application startup.

    ### Purpose:
    In Clean Architecture, domain entities remain agnostic of database
    mappings. To integrate with SQLAlchemy, mappings must be explicitly
    triggered to link ORM attributes to domain classes. Without this setup,
    attempts to interact with unmapped entities in database operations
    will lead to runtime errors.

    ### Solution:
    This function provides a single entry point to initialize the mapping
    of domain entities to database tables. By calling the `setup_map_tables` function,
    ORM attributes are linked to domain classes without altering domain code
    or introducing infrastructure concerns.

    ### Usage:
    Call the `setup_map_tables` function in the application factory to initialize
    mappings at startup. Additionally, it is necessary to call this function
    in `env.py` for Alembic migrations to ensure all models are available
    during database migrations.
    """
    map_users_table()
    map_chats_table()
    map_messages_table()


def setup_http_middlewares(app: FastAPI, /, api_config: ASGIConfig) -> None:
    """
    Registers all middlewares for FastAPI application.

    Args:
        app: FastAPI application
        api_config: ASGIConfig
    Returns:
        None
    """
    app.add_middleware(
        CORSMiddleware,  # type: ignore[arg-type, unused-ignore]
        allow_origins=[
            f"http://localhost:{api_config.port}",
            f"https://{api_config.host}:{api_config.port}",
            f"http://127.0.0.1:{api_config.port}",
            "http://127.0.0.1",
        ],
        allow_credentials=api_config.allow_credentials,
        allow_methods=api_config.allow_methods,
        allow_headers=api_config.allow_headers,
    )
    app.add_middleware(ASGIAuthMiddleware)  # type: ignore[arg-type, unused-ignore]
    app.add_middleware(ClientCacheMiddleware, max_age=60)  # type: ignore[arg-type, unused-ignore]
    app.add_middleware(LoggingMiddleware)  # type: ignore[arg-type, unused-ignore]


def setup_http_routes(app: FastAPI, /) -> None:
    """
    Registers all routers for FastAPI application

    Args:
        app: FastAPI application

    Returns:
        None
    """
    app.include_router(index.router)
    app.include_router(healthcheck.router)

    router_v1: APIRouter = APIRouter(prefix="/v1")
    router_v1.include_router(chat_router)

    app.include_router(router_v1)


def setup_http_exc_handlers(app: FastAPI, /) -> None:
    """
    Registers exception handlers for the FastAPI application.

    Args:
        app: FastAPI application instance to configure
    """
    exception_handler: ExceptionHandler = ExceptionHandler(app)
    exception_handler.setup_handlers()