from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.image import PositiveNumber, ImageName


@dataclass(eq=False)
class ImageEntity(BaseEntity):
    data: bytes
    width: PositiveNumber
    height: PositiveNumber
    name: ImageName
