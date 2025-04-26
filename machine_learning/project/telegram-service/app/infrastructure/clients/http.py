import logging
from typing import (
    Any,
    override,
)

import httpx
from httpx import (
    AsyncClient,
    Response,
)

from app.exceptions.infrastructure import (
    ClientConnectionException,
    ClientHTTPException,
)
from app.infrastructure.clients.base import (
    BaseClient,
    ClientResponse,
)


logger = logging.getLogger(__name__)


class HTTPXClient(BaseClient):
    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    @override
    async def get(self, url: str, **kwargs: Any) -> ClientResponse:
        try:
            wrapper = HTTPXClientResponseWrapper(await self._client.get(url, **kwargs))
            wrapper.raise_for_status()
            return wrapper

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error for URL %s: %s", url, str(e))
            raise ClientHTTPException(
                message=f"HTTP error {e.response.status_code} {url=}"
            ) from e

        except httpx.RequestError as e:
            logger.error("Connection error for URL %s: %s", url, str(e))
            raise ClientConnectionException(message=f"Connection failed, {url=}") from e

    @override
    async def post(self, url: str, data: Any = None, **kwargs: Any) -> ClientResponse:
        return HTTPXClientResponseWrapper(
            await self._client.post(url, data=data, **kwargs)
        )

    @override
    async def close(self) -> None:
        await self._client.aclose()


class HTTPXClientResponseWrapper(ClientResponse):
    def __init__(self, response: Response) -> None:
        self._response = response

    @override
    @property
    def status_code(self) -> int:
        return self._response.status_code

    @override
    def json(self) -> Any:
        return self._response.json()

    @override
    def raise_for_status(self) -> None:
        self._response.raise_for_status()