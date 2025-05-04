from typing import Annotated, Any, Self

from pydantic import BaseModel, PlainSerializer, PlainValidator, WithJsonSchema, Field

from app.domain.entities.image import ImageEntity


def hex_bytes_validator(o: Any) -> bytes:
    if isinstance(o, bytes):
        return o
    elif isinstance(o, bytearray):
        return bytes(o)
    elif isinstance(o, str):
        return bytes.fromhex(o)
    raise TypeError(type(o))


HexBytes = Annotated[
    bytes, PlainValidator(hex_bytes_validator), PlainSerializer(lambda b: b.hex()), WithJsonSchema({"type": "string"})
]


class ImageSchema(BaseModel):
    data: HexBytes = Field(..., description="photo data, represented in bytes")
    name: str = Field(..., min_length=1, description="name of the image")
    width: int = Field(..., ge=0, description="width of the image")
    height: int = Field(..., ge=0, description="height of the image")

    @classmethod
    def from_(cls, entity: ImageEntity) -> Self:
        return cls(
            data=entity.data,
            name=entity.name.as_generic_type(),
            width=entity.width.as_generic_type(),
            height=entity.height.as_generic_type(),
        )


class PhotoForSendToChatSchema(BaseModel):
    chat_id: int = Field(..., description="telegram chat id")
    image: ImageSchema

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int) -> Self:
        return cls(
            chat_id=chat_id,
            image=ImageSchema.from_(entity),
        )


class PhotoNewWidthNewHeightForSendToChatSchema(BaseModel):
    chat_id: int = Field(..., description="telegram chat id")
    image: ImageSchema
    new_width: int = Field(..., ge=0, description="new width of the image")
    new_height: int = Field(..., ge=0, description="new height of the image")

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int, new_width: int, new_height: int) -> Self:
        return cls(
            chat_id=chat_id,
            image=ImageSchema.from_(entity),
            new_width=new_width,
            new_height=new_height,
        )


class PairOfPhotosForStylizationAndForSendToChatSchema(BaseModel):
    original: ImageSchema
    style: ImageSchema
    chat_id: int = Field(..., description="telegram chat id")

    @classmethod
    def from_(cls, original: ImageEntity, style: ImageEntity, chat_id: int) -> Self:
        return cls(
            original=ImageSchema.from_(original),
            style=ImageSchema.from_(style),
            chat_id=chat_id,
        )

class PhotoForRotationSchema(BaseModel):
    chat_id: int = Field(..., description="telegram chat id")
    image: ImageSchema
    angle: int = Field(..., ge=0, le=360, description="angle of the image")

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int, angle: int) -> Self:
        return cls(
            chat_id=chat_id,
            image=ImageSchema.from_(entity),
            angle=angle,
        )