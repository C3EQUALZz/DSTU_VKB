import time
from typing import override, Final

from dishka import AsyncContainer
from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.infrastructure.metrics.base import BaseMetricsClient


class HTTPLatencyMetricsMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI,
            container: AsyncContainer
    ) -> None:
        super().__init__(app)
        self._container: Final[AsyncContainer] = container

    @override
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        metrics_client: BaseMetricsClient = await self._container.get(BaseMetricsClient)

        path: str = request.url.path
        method: str = request.method
        start_time: float = time.perf_counter()

        response: Response = await call_next(request)

        process_time: float = time.perf_counter() - start_time

        metrics_client.increment_http_requests(
            method=method,
            endpoint=path,
            status_code=response.status_code
        )

        metrics_client.observe_http_latency(
            method=method,
            endpoint=path,
            latency=process_time
        )

        return response
