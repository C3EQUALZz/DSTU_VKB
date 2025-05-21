from dataclasses import dataclass, field

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    name: str
    surname: str
    email: str
    password: str
    role: str = field(default="user", kw_only=True)


@dataclass(frozen=True)
class UpdateUserCommand(AbstractCommand):
    user_id: str
    name: str | None = field(default=None, kw_only=True)
    surname: str | None = field(default=None, kw_only=True)
    email: str | None = field(default=None, kw_only=True)
    role: str | None = field(default=None, kw_only=True)


@dataclass(frozen=True)
class DeleteUserCommand(AbstractCommand):
    user_id: str
