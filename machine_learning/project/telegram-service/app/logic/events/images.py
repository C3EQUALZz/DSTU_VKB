from dataclasses import dataclass

from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class ConvertedImageFromBrokerEvent(AbstractEvent):
    data: bytes
    name: str
    width: int
    height: int
    chat_id: int
