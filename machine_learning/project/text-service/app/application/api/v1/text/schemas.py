from typing import Self

from pydantic import BaseModel, Field

from app.domain.entities.message import TextMessageEntity


class TextMessageResponseSchemas(BaseModel):
    text: str = Field(..., min_length=1, description="Text which contains an answer from chat bot")

    @classmethod
    def from_entity(cls, text: TextMessageEntity) -> Self:
        return cls(text=text.content.as_generic_type())


class TextMessageRequestSchema(BaseModel):
    text: str = Field(..., min_length=1, description="Text which contains a question from user")
