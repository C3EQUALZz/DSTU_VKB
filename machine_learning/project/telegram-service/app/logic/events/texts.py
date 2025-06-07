from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class TextFromBrokerEvent(AbstractEvent):
    content: str
    chat_id: int
