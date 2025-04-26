import logging
from typing import Never

from fastapi import FastAPI, HTTPException, Request

from app.exceptions.base import BaseAppError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseAppError)
    async def app_base_exception_handler(request: Request, exc: BaseAppError) -> Never:
        logger.error(
            f"[{request.method}] {request.url} -> message: {exc.message}, status: {exc.status}"
        )

        if exc.headers is None:
            raise HTTPException(status_code=exc.status, detail=exc.message)

        raise HTTPException(
            status_code=exc.status, detail=exc.message, headers=exc.headers
        )
