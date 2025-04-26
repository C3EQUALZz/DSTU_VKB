from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel


class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, topic: str, value: BaseModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError
