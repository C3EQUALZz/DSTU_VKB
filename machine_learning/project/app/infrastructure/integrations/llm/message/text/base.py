from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.message import TextMessageEntity


class LLMTextMessageProvider(ABC):
    """Abstract class to provide working with large learning model"""

    @abstractmethod
    async def send_message(
            self,
            message: TextMessageEntity,
            temperature: float = 0.7,
            max_tokens: int = 150
    ) -> TextMessageEntity:
        """
        Sends message to llm and
        :param message: Message to send from user to chatbot
        :param temperature: Temperature to use
        :param max_tokens: Maximum number of tokens to use
        :return: Ответ API в виде словаря.
        """
        raise NotImplementedError
