from dataclasses import dataclass

from app.domain.entities.message import TextMessageEntity
from app.infrastructure.integrations.llm.dto.base import AbstractDTO


@dataclass(frozen=True)
class TextMessageDTO(AbstractDTO):
    message: TextMessageEntity
    temperature: float = 0.7
    max_tokens: int = 150
