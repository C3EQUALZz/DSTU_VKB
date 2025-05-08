from dataclasses import dataclass, field

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    name: str
    telegram_id: int | None = field(default=None, kw_only=True)
    role: str = field(default="user", kw_only=True)


@dataclass(frozen=True)
class UpdateUserCommand(AbstractCommand):
    user_id: str
    telegram_id: int | None = field(default=None, kw_only=True)
    first_name: str | None = field(default=None, kw_only=True)
    role: str | None = field(default=None, kw_only=True)


@dataclass(frozen=True)
class DeleteUserCommand(AbstractCommand):
    user_id: str
