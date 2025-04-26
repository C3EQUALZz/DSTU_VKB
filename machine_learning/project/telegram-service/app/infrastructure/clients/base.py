from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class BaseClient(ABC):
    @abstractmethod
    async def get(self, url: str, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def post(self, url: str, data: Any = None, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


class ClientResponse(ABC):
    @property
    @abstractmethod
    def status_code(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def json(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def raise_for_status(self):
        raise NotImplementedError