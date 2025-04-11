from abc import (
    ABC,
    abstractmethod,
)

from app.domain.entities.message import TextMessageEntity
from app.infrastructure.integrations.llm.dto.base import AbstractDTO


class BaseLLMProvider(ABC):
    """Abstract class to provide working with large learning model"""

    @abstractmethod
    async def send_message(self, dto: AbstractDTO) -> TextMessageEntity:
        """
        Sends message to llm and
        :param dto: Список сообщений (например, [{'role': 'user', 'content': 'Hello'}])
        :return: Ответ API в виде словаря.
        """
        raise NotImplementedError

