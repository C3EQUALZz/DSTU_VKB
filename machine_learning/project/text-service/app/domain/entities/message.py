from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.message import Text


@dataclass(eq=False)
class TextMessageEntity(BaseEntity):
    content: Text
