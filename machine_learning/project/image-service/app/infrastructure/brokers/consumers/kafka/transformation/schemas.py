from pydantic import BaseModel, Field

from app.infrastructure.brokers.consumers.kafka.base.schemas import ImageSchema


class CropImageAndSendToChatSchema(BaseModel):
    image: ImageSchema
    new_width: int = Field(..., gt=0, examples=[255], description="New image width for cropping")
    new_height: int = Field(..., gt=0, examples=[255], description="New image height for cropping")
    chat_id: int = Field(..., gt=0, description="telegram chat id")


class RotateImageAndSendToChatSchema(BaseModel):
    image: ImageSchema
    angle: int = Field(..., ge=0, le=360, examples=[0, 90, 180, 360], description="Rotation angle in degrees")
    chat_id: int = Field(..., gt=0, description="telegram chat id")
