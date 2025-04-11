from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class SendTextMessageToChatBot(AbstractCommand):
    content: str


@dataclass(frozen=True)
class SendVoiceMessageToChatBot(AbstractCommand):
    content: bytes
