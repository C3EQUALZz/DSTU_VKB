from abc import ABC, abstractmethod

from app.domain.entities.message import TextMessageEntity


class Translator(ABC):
    @abstractmethod
    async def translate_message(self, source: str, target: str, message: TextMessageEntity) -> TextMessageEntity:
        raise NotImplementedError
