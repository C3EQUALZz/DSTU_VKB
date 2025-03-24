from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import AsyncIterator


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop_consuming(self, topic: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop_consuming_all(self) -> None:
        raise NotImplementedError
