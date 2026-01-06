import logging
from typing import Final, override

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger: Final[logging.Logger] = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger.info("Request: method: %s, url: %s", request.method, request.url)
        response: Response = await call_next(request)
        logger.info("Response status %s", response.status_code)
        return response
