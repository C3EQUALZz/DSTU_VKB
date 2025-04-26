from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber, ImageName
from app.infrastructure.scheduler.tasks.schemas import PhotoForSendToChatSchema
from app.logic.commands.colorization import ConvertColorToGrayScaleAndSendToChatCommand, ConvertColorToGrayScaleCommand, \
    ConvertGrayScaleToColorCommand, ConvertGrayScaleToColorAndSendToChatCommand
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

        # For testing probably, this microservice will be used for integration with telegram

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

        # For testing probably, this microservice will be used for integration with telegram

        return self._image_colorization_service.convert_rgb_to_grayscale(
            image=image_entity
        )


class ConvertColorToGrayScaleAndSendToChatCommandHandler(
    ImageColorizationCommandHandler[ConvertColorToGrayScaleAndSendToChatCommand]
):
    async def __call__(self, command: ConvertColorToGrayScaleAndSendToChatCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.width),
            height=PositiveNumber(command.height),
            name=ImageName(command.name),
        )

        await self._scheduler.schedule_task(
            type(command),
            PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=command.chat_id),
        )


class ConvertGrayScaleToColorAndSendToChatCommandHandler(
    ImageColorizationCommandHandler[ConvertGrayScaleToColorAndSendToChatCommand]
):
    async def __call__(self, command: ConvertGrayScaleToColorAndSendToChatCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.width),
            height=PositiveNumber(command.height),
            name=ImageName(command.name),
        )

        await self._scheduler.schedule_task(
            type(command),
            PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=command.chat_id),
        )
