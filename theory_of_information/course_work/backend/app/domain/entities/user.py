from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.values.user import Email, Password, Role, Status


@dataclass(eq=False)
class UserEntity(BaseEntity):
    surname: str
    name: str
    patronymic: str
    email: Email
    password: Password
    role: Role = field(default_factory=lambda: Role("staffer"))
    status: Status = field(default_factory=lambda: Status("logged-in"))
