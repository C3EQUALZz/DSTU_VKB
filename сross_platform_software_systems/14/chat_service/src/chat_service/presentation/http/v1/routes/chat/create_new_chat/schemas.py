from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from chat_service.domain.chat.values.llm_provider import LLMProviderType


class CreateChatRequestSchema(BaseModel):
    llm_provider: Annotated[
        LLMProviderType | None,
        Field(
            examples=["xiaomi/mimo-v2-flash:free"],
            description="Model for processing response"
        )
    ] = None


class CreateChatResponseSchema(BaseModel):
    chat_id: Annotated[
        UUID,
        Field(
            examples=["2e6bd346-d7e7-421a-8983-8fb5c2426ad0"],
            description="Unique chat ID in system"
        )
    ]
