from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class VerifyUserCredentialsCommand(AbstractCommand):
    name: str
    password: str


@dataclass(frozen=True)
class RegisterUserCommand(AbstractCommand):
    name: str
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserCommand(AbstractCommand):
    name: str
    email: str
    password: str