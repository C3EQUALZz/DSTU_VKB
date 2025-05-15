import uuid
from typing import Literal

from pydantic import BaseModel, Field

from app.infrastructure.brokers.consumers.kafka.base.schemas import StringUUID


class UserStartsBotSchema(BaseModel):
    event_id: StringUUID
    user_id: StringUUID = Field(default_factory=lambda: uuid.uuid4())
    telegram_id: int = Field(..., ge=0, description="Telegram id of the user.")
