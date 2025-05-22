from pydantic import BaseModel, Field

from app.application.api.v1.utils.schemas import StringUUID


class SendMessageToTelegramSchema(BaseModel):
    event_id: StringUUID
    telegram_id: int = Field(..., ge=0, description="Telegram ID of user")
    message: str = Field(..., description="Message text for user")
