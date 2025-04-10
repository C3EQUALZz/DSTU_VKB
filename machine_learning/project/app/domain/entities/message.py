from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.message import Text


@dataclass(eq=False)
class MessageEntity(BaseEntity):
    chat_oid: str
    text: Text


@dataclass(eq=False)
class ImageMessageEntity(BaseEntity):
    chat_oid: str
    photo: bytes
