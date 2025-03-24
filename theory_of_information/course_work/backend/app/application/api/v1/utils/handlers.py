from fastapi import FastAPI, Request, HTTPException
import logging

from app.exceptions.base import BaseAppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseAppException)
    async def app_base_exception_handler(request: Request, exc: BaseAppException):
        logger.error(f"[{request.method}] {request.url} -> message: {exc.message}, status: {exc.status}")

        if exc.headers is None:
            raise HTTPException(status_code=exc.status, detail=exc.message)

        raise HTTPException(status_code=exc.status, detail=exc.message, headers=exc.headers)
