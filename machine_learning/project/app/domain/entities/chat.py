from dataclasses import (
    dataclass,
    field,
)

from app.domain.entities.base import BaseEntity
from app.domain.entities.message import (
    ImageMessageEntity,
    TextMessageEntity,
)
from app.domain.entities.user import UserEntity
from app.domain.values.chat import (
    ChatType,
    Title,
)


@dataclass(eq=False)
class ChatEntity(BaseEntity):
    title: Title
    chat_type: ChatType
    users: list[UserEntity] = field(default_factory=list, kw_only=True)
    messages: list[TextMessageEntity] = field(default_factory=list, kw_only=True)
    photos: list[ImageMessageEntity] = field(default_factory=list, kw_only=True)
