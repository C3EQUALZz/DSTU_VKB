from typing import Protocol
from abc import abstractmethod

from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.values.chat_id import ChatID


class ChatCommandGateway(Protocol):
    @abstractmethod
    async def add(self, chat: Chat) -> None:
        ...

    @abstractmethod
    async def read_by_id(self, chat_id: ChatID) -> Chat | None:
        ...

    @abstractmethod
    async def update(self, chat: Chat) -> None:
        ...

    @abstractmethod
    async def delete_by_id(self, chat_id: ChatID) -> None:
        ...
