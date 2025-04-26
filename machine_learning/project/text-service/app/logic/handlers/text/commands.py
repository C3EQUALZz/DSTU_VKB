from app.domain.entities.message import TextMessageEntity
from app.domain.values.message import Text

from app.logic.commands.text import (
    SendTextMessageToChatBotCommand,
    TranslateTextCommand,
    SendTextMessageToChatBotAndThenReplyInMessengerCommand
)

from app.logic.dtos.chatbot import MessageAndChatIDDTO
from app.logic.handlers.text.base import TextsCommandHandler


class SendTextMessageToChatBotCommandHandler(TextsCommandHandler[SendTextMessageToChatBotCommand]):
    async def __call__(self, command: SendTextMessageToChatBotCommand) -> TextMessageEntity:
        text_entity: TextMessageEntity = TextMessageEntity(content=Text(command.content))
        return await self._text_service.send_text_message_to_chat_bot(text_entity)


class SendTextMessageToChatBotAndThenReplyInMessengerCommandHandler(
    TextsCommandHandler[SendTextMessageToChatBotAndThenReplyInMessengerCommand]
):
    async def __call__(self, command: SendTextMessageToChatBotAndThenReplyInMessengerCommand) -> MessageAndChatIDDTO:
        text_entity: TextMessageEntity = TextMessageEntity(content=Text(command.content))
        answer_from_bot: TextMessageEntity = await self._text_service.send_text_message_to_chat_bot(text_entity)

        return MessageAndChatIDDTO(
            content=answer_from_bot.content.as_generic_type(),
            chat_id=command.chat_id
        )


class TranslateMessageCommandHandler(TextsCommandHandler[TranslateTextCommand]):
    async def __call__(self, command: TranslateTextCommand) -> TextMessageEntity:
        text_entity: TextMessageEntity = TextMessageEntity(content=Text(command.content))
        return await self._text_service.translate_message(
            message=text_entity,
            target=command.target,
        )
