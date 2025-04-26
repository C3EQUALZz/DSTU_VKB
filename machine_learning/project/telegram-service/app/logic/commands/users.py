from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    user_id: str
    full_name: str
    user_login: str


@dataclass(frozen=True)
class DeleteUserCommand(AbstractCommand):
    user_id: str
