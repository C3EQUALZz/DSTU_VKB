from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.values.user import UserName, UserSurname, UserEmail, UserPassword, UserRole


@dataclass(eq=False)
class UserEntity(BaseEntity):
    name: UserName
    surname: UserSurname
    email: UserEmail
    password: UserPassword
    telegram_id: int | None = field(default=None)
    role: UserRole = field(default_factory=lambda: UserRole("user"))
    is_verified: bool = field(default=False)
