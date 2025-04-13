from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.message import Text


@dataclass(eq=False)
class TextMessageEntity(BaseEntity):
    content: Text
    role: str


@dataclass(eq=False)
class ImageMessageEntity(BaseEntity):
    photo: bytes
    chat_id: int


@dataclass(eq=False)
class VoiceMessageEntity(BaseEntity):
    chat_oid: str
    voice: bytes
