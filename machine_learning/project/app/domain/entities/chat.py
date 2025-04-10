from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.entities.message import MessageEntity
from app.domain.values.chat import Title


@dataclass(eq=False)
class ChatEntity(BaseEntity):
    title: Title
    messages: list[MessageEntity] = field(default_factory=list, kw_only=True)