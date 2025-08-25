from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpView:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserView:
    user_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class UserView:
    first_name: str
    role: str
    language: str
    telegram_id: int | None = field(default=None)
