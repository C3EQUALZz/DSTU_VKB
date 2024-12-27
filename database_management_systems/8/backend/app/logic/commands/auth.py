from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class VerifyUserCredentialsCommand(AbstractCommand):
    name: str
    password: str
