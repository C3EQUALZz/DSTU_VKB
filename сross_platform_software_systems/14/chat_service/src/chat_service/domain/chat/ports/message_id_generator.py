from abc import abstractmethod
from typing import Protocol

from chat_service.domain.chat.values.message_id import MessageID


class MessageIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> MessageID:
        ...
