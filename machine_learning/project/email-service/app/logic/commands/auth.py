from dataclasses import dataclass

from app.logic.commands.base import BaseCommand


@dataclass(frozen=True)
class SendVerificationEmailCommand(BaseCommand):
    email: str
    name: str
    surname: str
    url: str
