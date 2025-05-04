from typing import Annotated, Any

from pydantic import PlainValidator, PlainSerializer, WithJsonSchema, BaseModel, Field


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
    data: HexBytes
    name: str = Field(..., min_length=1, description="name of the image")
    width: int = Field(..., gt=0, description="width of the image")
    height: int = Field(..., gt=0, description="height of the image")


class ImageWithTelegramChatId(ImageSchema):
    chat_id: int = Field(..., gt=0, description="telegram chat_id of person who requested the image")
