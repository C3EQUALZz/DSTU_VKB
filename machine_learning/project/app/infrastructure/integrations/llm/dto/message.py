from app.domain.entities.message import MessageEntity
from app.infrastructure.integrations.llm.dto.base import AbstractDTO
from dataclasses import dataclass

@dataclass(frozen=True)
class TextMessageDTO(AbstractDTO):
    message: MessageEntity
    temperature: float = 0.7
    max_tokens: int = 150
