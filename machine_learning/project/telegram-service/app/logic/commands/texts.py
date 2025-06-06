from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class SendTextMessageToChatBotCommand(AbstractCommand):
    content: str
    chat_id: int
