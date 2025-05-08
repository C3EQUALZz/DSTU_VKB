from app.logic.commands.base import BaseCommand
from dataclasses import dataclass


@dataclass(frozen=True)
class UserRegisterCommand(BaseCommand):
    name: str
    surname: str
    email: str
    password: str
