from app.domain.entities.message import TextMessageEntity
from app.exceptions.infrastructure import ChatModelIsBusyError
from app.infrastructure.integrations.text_large_learning_models.base import LLMTextMessageModel
from app.infrastructure.integrations.translation.base import Translator


class TextMessageService:
    def __init__(
            self,
            chat_bot_model: LLMTextMessageModel,
            translator: Translator,
    ) -> None:
        self._chat_bot_provider = chat_bot_model
        self._translator = translator

    async def send_text_message_to_chat_bot(self, message: TextMessageEntity) -> TextMessageEntity:
        """
        This method is used to send a text message for chat bot.
        :param message: entity message to be sent
        :return:
        """
        if result := await self._chat_bot_provider.send_message(message=message):
            return result
        raise ChatModelIsBusyError("chat model is busy, please try again later")

    async def translate_message(
            self,
            target: str,
            message: TextMessageEntity,
            source: str = "auto"
    ) -> TextMessageEntity:
        return await self._translator.translate_message(message=message, target=target, source=source)
