from typing import Annotated

from pydantic import BaseModel, Field

from chat_service.domain.chat.values.llm_provider import LLMProviderType


class ChangeChatLLMProviderRequestSchema(BaseModel):
    llm_provider: Annotated[
        LLMProviderType,
        Field(
            examples=["xiaomi/mimo-v2-flash:free"],
            description="Model for processing response"
        )
    ]
