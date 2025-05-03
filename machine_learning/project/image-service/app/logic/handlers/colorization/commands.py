from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber, ImageName
from app.logic.commands.colorization import (
    ConvertColorToGrayScaleCommand,
    ConvertGrayScaleToColorCommand,
    StylizeCommand
)
from app.logic.handlers.colorization.base import ImageColorizationCommandHandler


class ConvertColorToGrayScaleCommandHandler(
    ImageColorizationCommandHandler[ConvertColorToGrayScaleCommand],
):
    async def __call__(self, command: ConvertColorToGrayScaleCommand) -> ImageEntity:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.width),
            height=PositiveNumber(command.height),
            name=ImageName(command.name),
        )

        return self._image_colorization_service.convert_rgb_to_grayscale(
            image=image_entity
        )


class ConvertGrayScaleToColorCommandHandler(
    ImageColorizationCommandHandler[ConvertGrayScaleToColorCommand],
):
    async def __call__(self, command: ConvertGrayScaleToColorCommand) -> ImageEntity:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.width),
            height=PositiveNumber(command.height),
            name=ImageName(command.name),
        )

        return self._image_colorization_service.convert_rgb_to_grayscale(
            image=image_entity
        )


class StylizeCommandHandler(
    ImageColorizationCommandHandler[StylizeCommand],
):
    async def __call__(self, command: StylizeCommand) -> ImageEntity:
        original_image_entity: ImageEntity = ImageEntity(
            data=command.original_image_data,
            width=PositiveNumber(command.original_width),
            height=PositiveNumber(command.original_height),
            name=ImageName(command.original_name)
        )

        style_image_entity: ImageEntity = ImageEntity(
            data=command.style_image_data,
            width=PositiveNumber(command.style_width),
            height=PositiveNumber(command.style_height),
            name=ImageName(command.style_name)
        )

        return self._image_colorization_service.style_image(
            original_image=original_image_entity,
            styling_template=style_image_entity,
        )
