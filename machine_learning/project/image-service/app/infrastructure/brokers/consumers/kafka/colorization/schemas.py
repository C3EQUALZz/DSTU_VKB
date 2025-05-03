from pydantic import BaseModel, Field

from app.infrastructure.brokers.consumers.kafka.base.schemas import ImageSchema


class ConvertColorImageSchema(BaseModel):
    image: ImageSchema
    chat_id: int = Field(..., ge=0, description="chat id of the image")


class StylizeImageSchema(BaseModel):
    original_image: ImageSchema
    style_image: ImageSchema
    chat_id: int = Field(..., ge=0, description="chat id of the image")
