from dataclasses import dataclass, field

from app.domain.values.user import Role, Email, Password

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class UserEntity(BaseEntity):
    name: str
    surname: str
    email: Email
    password: Password
    role: Role = field(default_factory=lambda: Role("user"))
