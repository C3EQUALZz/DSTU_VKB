from app.domain.entities.message import TextMessageEntity
from app.domain.values.message import Text
from app.infrastructure.brokers.publishers.schemas.text import ReplyFromLLMToChatSchema
from app.logic.events.texts import SendMessageForLLMFromBrokerEvent
from app.logic.handlers.text.base import TextsEventHandler


class SendTextMessageToChatBotEventHandler(TextsEventHandler[SendMessageForLLMFromBrokerEvent]):
    async def __call__(self, event: SendMessageForLLMFromBrokerEvent) -> None:
        text_entity: TextMessageEntity = TextMessageEntity(content=Text(event.content))
        reply_from_bot: TextMessageEntity = await self._text_service.send_text_message_to_chat_bot(text_entity)
        topic: str = self._factory.get_topic(self.__class__)
        await self._broker.send_message(
            topic=topic,
            value=ReplyFromLLMToChatSchema(
                content=reply_from_bot.content.as_generic_type(),
                chat_id=event.chat_id,
            )
        )
