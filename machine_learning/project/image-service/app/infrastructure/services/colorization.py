from app.domain.entities.image import ImageEntity
from app.infrastructure.integrations.color_to_gray.base import BaseImageColorToCrayScaleConverter
from app.infrastructure.integrations.gray_to_color.base import BaseImageGrayScaleToColorConverter


class ImageColorizationService:
    def __init__(
            self,
            gray_to_color_converter: BaseImageGrayScaleToColorConverter,
            color_to_gray_converter: BaseImageColorToCrayScaleConverter,
    ) -> None:
        self._color_to_gray_converter = color_to_gray_converter
        self._gray_to_color_converter = gray_to_color_converter

    def convert_grayscale_to_rgb(self, image: ImageEntity) -> ImageEntity:
        data: bytes = self._gray_to_color_converter.process(input_data=image.data)
        return ImageEntity(data=data, width=image.width, height=image.height, name=image.name)

    def convert_rgb_to_grayscale(self, image: ImageEntity) -> ImageEntity:
        return self._color_to_gray_converter.convert(image=image)
