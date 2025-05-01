from dataclasses import dataclass, field

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    user_id: int
    full_name: str
    user_login: str
    language_code: str
    role: str


@dataclass(frozen=True)
class DeleteUserCommand(AbstractCommand):
    user_id: int


@dataclass(frozen=True)
class UpdateUserCommand(CreateUserCommand):
    ...
