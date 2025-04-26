from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.message import Text


@dataclass(eq=False)
class TextMessageEntity(BaseEntity):
    content: Text
    role: str


@dataclass(eq=False)
class ImageEntity(BaseEntity):
    data: bytes
    name: str
    height: int
    width: int


@dataclass(eq=False)
class VoiceMessageEntity(BaseEntity):
    chat_oid: str
    voice: bytes
