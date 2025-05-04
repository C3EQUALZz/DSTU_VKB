from typing import (
    Annotated,
    Any,
    Self,
)

from pydantic import (
    BaseModel,
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

class ImageSchema(BaseModel):
    data: HexBytes
    width: int
    height: int
    name: str

    @classmethod
    def from_(cls, entity: ImageEntity) -> Self:
        return cls(
            data=entity.data,
            width=entity.width,
            height=entity.height,
            name=entity.name,
        )



class ConvertColorImageToGrayScaleSchema(BaseModel):
    image: ImageSchema
    chat_id: int

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int) -> Self:
        return cls(
            image=ImageSchema.from_(entity=entity),
            chat_id=chat_id,
        )

class MetadataImageSchema(ConvertColorImageToGrayScaleSchema):
    ...


class ConvertGrayScaleToColorSchema(ConvertColorImageToGrayScaleSchema):
    ...


class CropImageSchema(BaseModel):
    image: ImageSchema
    new_width: int
    new_height: int
    chat_id: int

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int, new_width: int, new_height: int) -> Self:
        return cls(
            image=ImageSchema.from_(entity=entity),
            new_width=new_width,
            new_height=new_height,
            chat_id=chat_id,
        )


class RotateImageSchema(BaseModel):
    image: ImageSchema
    chat_id: int
    angle: int

    @classmethod
    def from_(cls, entity: ImageEntity, chat_id: int, angle: int) -> Self:
        return cls(
            image=ImageSchema.from_(entity=entity),
            chat_id=chat_id,
            angle=angle,
        )
