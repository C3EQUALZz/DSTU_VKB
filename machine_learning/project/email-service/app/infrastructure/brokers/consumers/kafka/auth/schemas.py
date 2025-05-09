from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl

from app.infrastructure.brokers.consumers.kafka.base import StringUUID


class UserSendEmailForVerificationSchema(BaseModel):
    event_id: StringUUID = Field(..., description="Unique ID of an event")
    name: str = Field(..., min_length=1, max_length=255, description="User name for email")
    surname: str = Field(..., min_length=1, max_length=255, description="User surname for email")
    email: EmailStr = Field(..., description="Email address for sending verification email")
    url: AnyHttpUrl = Field(..., description="URL endpoint for verifying user. This url must be in email")
