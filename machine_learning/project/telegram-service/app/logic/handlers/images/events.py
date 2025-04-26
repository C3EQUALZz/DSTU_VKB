from app.domain.entities.message import ImageEntity
from app.infrastructure.scheduler.tasks.images.schemas import ImageForSendToChatSchema
from app.logic.events.images import (
    ConvertColorImageToGrayScaleImageEvent,
    ConvertGrayScaleImageToColorImageEvent,
    CropImageEvent,
    GetMetadataFromImageEvent,
    RotateImageEvent,
)
from app.logic.handlers.images.base import ImagesEventHandler
from app.settings.configs.enums import TaskNamesConfig


class ConvertColorImageToGrayScaleImageEventHandler(ImagesEventHandler[ConvertColorImageToGrayScaleImageEvent]):
    async def __call__(self, event: ConvertColorImageToGrayScaleImageEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            name=event.name,
            height=event.height,
            width=event.width,
        )

        await self._scheduler.schedule_task(
            TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER,
            schemas=ImageForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class GetMetadataFromImageEventHandler(ImagesEventHandler[GetMetadataFromImageEvent]):
    async def __call__(self, event: GetMetadataFromImageEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            name=event.name,
            height=event.height,
            width=event.width,
        )

        await self._scheduler.schedule_task(
            TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER,
            schemas=ImageForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class ConvertGrayScaleImageToColorImageEventHandler(ImagesEventHandler[ConvertGrayScaleImageToColorImageEvent]):
    async def __call__(self, event: ConvertGrayScaleImageToColorImageEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            name=event.name,
            height=event.height,
            width=event.width,
        )

        await self._scheduler.schedule_task(
            TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER,
            schemas=ImageForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class CropImageEventHandler(ImagesEventHandler[CropImageEvent]):
    async def __call__(self, event: CropImageEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            name=event.name,
            height=event.height,
            width=event.width,
        )

        await self._scheduler.schedule_task(
            TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER,
            schemas=ImageForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class RotateImageEventHandler(ImagesEventHandler[RotateImageEvent]):
    async def __call__(self, event: RotateImageEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            name=event.name,
            height=event.height,
            width=event.width,
        )

        await self._scheduler.schedule_task(
            TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER,
            schemas=ImageForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )
