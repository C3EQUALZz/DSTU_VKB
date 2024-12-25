from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateUserCommand(AbstractCommand):
    name: str
    password: str
    email: str


@dataclass(frozen=True)
class UpdateUserCommand(AbstractCommand):
    oid: str
    name: str
    password: str
    email: str


@dataclass(frozen=True)
class DeleteUserCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class GetUserByIdCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class GetAllUsersCommand(AbstractCommand): ...


@dataclass(frozen=True)
class VerifyUserCredentialsCommand(AbstractCommand):
    name: str
    password: str
