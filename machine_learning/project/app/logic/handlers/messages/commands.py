from app.domain.entities.message import TextMessageEntity
from app.domain.values.message import Text
from app.infrastructure.services.message import MessageService
from app.logic.commands.messages import SendTextMessageToChatBot
from app.logic.handlers.messages.base import MessagesCommandHandler


class SendTextMessageCommandHandler(MessagesCommandHandler[SendTextMessageToChatBot]):
    async def __call__(self, command: SendTextMessageToChatBot) -> TextMessageEntity:
        text_chat_bot_service: MessageService = MessageService(self._text_llm)
        text_entity: TextMessageEntity = TextMessageEntity(content=Text(command.content), role="user")
        return await text_chat_bot_service.send_text_message(text_entity)
