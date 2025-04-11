from abc import ABC, abstractmethod

from app.domain.entities.message import MessageEntity
from app.infrastructure.integrations.llm.dto.base import AbstractDTO


class BaseLLMProvider(ABC):
    """Абстрактный класс для LLM провайдеров, с асинхронными вызовами API."""

    @abstractmethod
    async def send_message(self, dto: AbstractDTO) -> MessageEntity:
        """
        Отправляет запрос на создание ответа по диалогу.
        :param dto: Список сообщений (например, [{'role': 'user', 'content': 'Hello'}])
        :return: Ответ API в виде словаря.
        """
        raise NotImplementedError

