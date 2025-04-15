from typing import Annotated, Any, Self

from pydantic import BaseModel, PlainSerializer, PlainValidator, WithJsonSchema

from app.domain.entities.message import ImageMessageEntity


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


class ColorizePhotoSchema(BaseModel):
    chat_id: int
    photo: HexBytes

    @classmethod
    def from_entity(cls, entity: ImageMessageEntity) -> Self:
        return cls(chat_id=entity.chat_id, photo=entity.photo)
