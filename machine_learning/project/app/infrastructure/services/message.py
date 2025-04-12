from app.domain.entities.message import TextMessageEntity
from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageProvider


class MessageService:
    def __init__(self, text_llm: LLMTextMessageProvider) -> None:
        self._text_provider = text_llm

    async def send_text_message(self, message: TextMessageEntity) -> TextMessageEntity:
        """
        This method is used to send a text message for chat bot.
        :param message: entity message to be sent
        :return:
        """
        return await self._text_provider.send_message(message=message)