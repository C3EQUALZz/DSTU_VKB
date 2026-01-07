from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class RequestToUserMessageRequestSchema(BaseModel):
    content: Annotated[
        str,
        Field(
            min_length=1,
            examples=["Hello. How are you?"],
            description="Message content from user",
        )
    ]


class RequestToUserMessageResponseSchema(BaseModel):
    user_message_id: UUID
    assistant_message_id: UUID
    assistant_message_content: str
