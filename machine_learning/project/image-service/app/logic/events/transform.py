from dataclasses import dataclass
from app.logic.events.base import AbstractEvent


@dataclass(frozen=True)
class CropImageAndSendToChatEvent(AbstractEvent):
    data: bytes
    name: str
    old_width: int
    old_height: int
    new_width: int
    new_height: int
    chat_id: int


@dataclass(frozen=True)
class RotateImageAndSendToChatEvent(AbstractEvent):
    data: bytes
    name: str
    width: int
    height: int
    angle: int
    chat_id: int


