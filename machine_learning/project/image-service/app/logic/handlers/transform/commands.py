from typing import override

from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber, ImageName
from app.infrastructure.scheduler.tasks.schemas import PhotoForSendToChatSchema
from app.logic.commands.transform import CropImageCommand, RotateImageCommand, CropImageAndSendToChatCommand, \
    RotateImageAndSendToChatCommand
from app.logic.handlers.transform.base import ImageTransformCommandHandler


class CropImageCommandHandler(ImageTransformCommandHandler[CropImageCommand]):
    @override
    async def __call__(self, command: CropImageCommand) -> ImageEntity:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.old_width),
            height=PositiveNumber(command.old_height),
            name=ImageName(command.name),
        )

        return self._image_transform_service.crop(
            image=image_entity,
            new_width=command.new_width,
            new_height=command.new_height
        )


class CropImageAndSendToChatCommandHandler(
    ImageTransformCommandHandler[CropImageAndSendToChatCommand]
):
    async def __call__(self, command: CropImageAndSendToChatCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.old_width),
            height=PositiveNumber(command.old_height),
            name=ImageName(command.name),
        )

        await self._scheduler.schedule_task(
            name=type(command),
            schemas=PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=command.chat_id),
        )


class RotateImageCommandHandler(ImageTransformCommandHandler[RotateImageCommand]):
    @override
    async def __call__(self, command: RotateImageCommand) -> ImageEntity:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.width),
            height=PositiveNumber(command.height),
            name=ImageName(command.name),
        )

        return self._image_transform_service.rotate(
            image=image_entity,
            angle=command.angle,
        )


class RotateImageAndSendToChatCommandHandler(
    ImageTransformCommandHandler[RotateImageAndSendToChatCommand]
):
    async def __call__(self, command: RotateImageAndSendToChatCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            width=PositiveNumber(command.width),
            height=PositiveNumber(command.height),
            name=ImageName(command.name),
        )

        await self._scheduler.schedule_task(
            name=type(command),
            schemas=PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=command.chat_id),
        )


