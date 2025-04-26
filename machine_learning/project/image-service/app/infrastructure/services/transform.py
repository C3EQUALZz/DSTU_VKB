from typing import Final

from app.domain.entities.image import ImageEntity
from app.infrastructure.integrations.crop.base import BaseImageCropConverter
from app.infrastructure.integrations.rotation.base import BaseImageRotationConverter


class ImageTransformService:
    def __init__(
            self,
            crop_converter: BaseImageCropConverter,
            rotation_converter: BaseImageRotationConverter,
    ) -> None:
        self._crop_converter: Final[BaseImageCropConverter] = crop_converter
        self._rotation_converter: Final[BaseImageRotationConverter] = rotation_converter

    def crop(self, image: ImageEntity, new_width: int, new_height: int) -> ImageEntity:
        return self._crop_converter.convert(image=image, new_width=new_width, new_height=new_height)

    def rotate(self, image: ImageEntity, angle: int = 90) -> ImageEntity:
        return self._rotation_converter.convert(image=image, angle=angle)
