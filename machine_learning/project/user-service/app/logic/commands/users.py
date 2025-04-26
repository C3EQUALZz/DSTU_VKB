from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    first_name: str


@dataclass(frozen=True)
class UpdateUserCommand(AbstractCommand):
    oid: str
    first_name: str
    role: str


@dataclass(frozen=True)
class DeleteUserCommand(AbstractCommand):
    oid: str
