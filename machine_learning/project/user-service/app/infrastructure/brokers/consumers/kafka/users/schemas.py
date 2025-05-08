import uuid
from typing import Literal

from pydantic import BaseModel, Field

from app.infrastructure.brokers.consumers.kafka.base.schemas import StringUUID


class UserSchemaEvent(BaseModel):
    event_id: StringUUID
    user_id: StringUUID = Field(default_factory=lambda: uuid.uuid4())
    first_name: str = Field(..., min_length=1, max_length=255, description="First name of the user.")
    telegram_id: int = Field(..., ge=0, description="Telegram id of the user.")
    role: Literal["user", "admin"] = Field(
        default="user",
        min_length=1,
        max_length=255,
        description="Role of the user."
    )
