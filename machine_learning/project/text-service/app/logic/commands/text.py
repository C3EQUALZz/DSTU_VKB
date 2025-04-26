from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class SendTextMessageToChatBotCommand(AbstractCommand):
    content: str


@dataclass(frozen=True)
class TranslateTextCommand(AbstractCommand):
    content: str
    target: str


@dataclass(frozen=True)
class SendTextMessageToChatBotAndThenReplyInMessengerCommand(AbstractCommand):
    content: str
    chat_id: int
