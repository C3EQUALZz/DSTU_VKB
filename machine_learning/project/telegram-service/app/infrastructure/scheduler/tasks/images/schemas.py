from typing import (
    Annotated,
    Any,
    Self,
)

from pydantic import (
    BaseModel,
    Field,
    PlainSerializer,
    PlainValidator,
    WithJsonSchema,
)

from app.domain.entities.message import ImageEntity


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


class ImageForSendToChatSchema(BaseModel):
    chat_id: int = Field(..., description="telegram chat id")
    data: HexBytes = Field(..., description="photo data, represented in bytes")
    name: str = Field(default="converted.jpg", min_length=1, description="name of the image", validate_default=True)

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int) -> Self:
        return cls(
            chat_id=chat_id,
            data=entity.data,
            name=entity.name,
        )
