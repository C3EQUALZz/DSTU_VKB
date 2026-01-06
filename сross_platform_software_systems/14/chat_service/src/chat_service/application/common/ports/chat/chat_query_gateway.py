from abc import abstractmethod
from typing import Protocol

from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.values.chat_id import ChatID


class ChatQueryGateway(Protocol):
    @abstractmethod
    async def read_by_id(self, chat_id: ChatID) -> Chat | None:
        ...

    @abstractmethod
    async def read_all(self) -> list[Chat] | None:
        ...
