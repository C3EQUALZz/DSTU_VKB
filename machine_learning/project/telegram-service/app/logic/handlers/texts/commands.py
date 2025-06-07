from app.infrastructure.brokers.schemas.texts import MessageLLMSchema
from app.logic.commands.texts import SendTextMessageToChatBotCommand
from app.logic.handlers.texts.base import TextsCommandHandler


class SendTextMessageToChatBotCommandHandler(TextsCommandHandler[SendTextMessageToChatBotCommand]):
    async def __call__(self, command: SendTextMessageToChatBotCommand) -> None:
        topic: str = self._topic_command_handler_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=MessageLLMSchema(chat_id=command.chat_id, content=command.content),
        )
