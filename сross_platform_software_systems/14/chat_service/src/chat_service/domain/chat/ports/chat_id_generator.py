from typing import Protocol
from abc import abstractmethod

from chat_service.domain.chat.values.chat_id import ChatID


class ChatIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> ChatID:
        ...
