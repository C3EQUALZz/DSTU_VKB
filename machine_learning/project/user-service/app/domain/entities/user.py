from dataclasses import dataclass, field

from app.domain.values.user import Role

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class UserEntity(BaseEntity):
    first_name: str
    role: Role = field(default_factory=lambda: Role("user"))
