from dataclasses import (
    dataclass,
    field,
)

from app.domain.entities.base import BaseEntity
from app.domain.entities.message import TextMessageEntity


@dataclass(eq=False)
class UserEntity(BaseEntity):
    surname: str
    name: str
    messages: list[TextMessageEntity] = field(default_factory=list, kw_only=True)
