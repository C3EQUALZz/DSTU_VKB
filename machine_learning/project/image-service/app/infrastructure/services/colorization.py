from typing import Final

from app.domain.entities.image import ImageEntity
from app.infrastructure.integrations.color_to_gray.base import BaseImageColorToCrayScaleConverter
from app.infrastructure.integrations.gray_to_color.base import BaseImageGrayScaleToColorConverter
from app.infrastructure.integrations.inversion.base import BaseImageInversionConverter
from app.infrastructure.integrations.stylization.base import BaseImageStylizationConverter


class ImageColorizationService:
    def __init__(
            self,
            gray_to_color_converter: BaseImageGrayScaleToColorConverter,
            color_to_gray_converter: BaseImageColorToCrayScaleConverter,
            stylization_converter: BaseImageStylizationConverter,
            inversion_converter: BaseImageInversionConverter,
    ) -> None:
        self._color_to_gray_converter: Final[BaseImageColorToCrayScaleConverter] = color_to_gray_converter
        self._gray_to_color_converter: Final[BaseImageGrayScaleToColorConverter] = gray_to_color_converter
        self._stylization_converter: Final[BaseImageStylizationConverter] = stylization_converter
        self._inversion_converter: Final[BaseImageInversionConverter] = inversion_converter

    def convert_grayscale_to_rgb(self, image: ImageEntity) -> ImageEntity:
        data: bytes = self._gray_to_color_converter.process(input_data=image.data)
        return ImageEntity(data=data, width=image.width, height=image.height, name=image.name)

    def convert_rgb_to_grayscale(self, image: ImageEntity) -> ImageEntity:
        return self._color_to_gray_converter.convert(image=image)

    def style_image(self, original_image: ImageEntity, styling_template: ImageEntity) -> ImageEntity:
        data: bytes = self._stylization_converter.process(
            content_data=original_image.data,
            style_data=styling_template.data
        )

        return ImageEntity(
            data=data,
            width=original_image.width,
            height=original_image.height,
            name=original_image.name
        )

    def inverse_image(self, original_image: ImageEntity) -> ImageEntity:
        return self._inversion_converter.convert(image=original_image)
