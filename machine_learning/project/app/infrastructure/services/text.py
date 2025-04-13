from app.domain.entities.message import TextMessageEntity
from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageModel


class TextMessageService:
    def __init__(self, chat_bot_model: LLMTextMessageModel) -> None:
        self._chat_bot_provider = chat_bot_model

    async def send_text_message_to_chat_bot(self, message: TextMessageEntity) -> TextMessageEntity:
        """
        This method is used to send a text message for chat bot.
        :param message: entity message to be sent
        :return:
        """
        return await self._chat_bot_provider.send_message(message=message)
