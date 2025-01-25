from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.middlewares.client_cache import ClientCacheMiddleware


def setup_middlewares(app: FastAPI) -> None:
    # Client cache setup
    app.add_middleware(ClientCacheMiddleware, max_age=60)  # type: ignore

    # CORS setup
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                       "Access-Control-Allow-Origin",
                       "Authorization", "Cache-Control"]
    )
