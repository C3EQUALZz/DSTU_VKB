from app.domain.entities.message import TextMessageEntity
from app.domain.values.message import Text
from app.logic.commands.texts import SendTextMessageToChatBotCommand
from app.logic.handlers.texts.base import TextsCommandHandler


class SendTextMessageToChatBotCommandHandler(TextsCommandHandler[SendTextMessageToChatBotCommand]):
    async def __call__(self, command: SendTextMessageToChatBotCommand) -> TextMessageEntity:
        ...
