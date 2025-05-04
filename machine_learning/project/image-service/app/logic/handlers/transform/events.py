from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber, ImageName
from app.infrastructure.scheduler.tasks.schemas import PhotoForSendToChatSchema, PhotoForRotationSchema
from app.logic.events.transform import CropImageAndSendToChatEvent, RotateImageAndSendToChatEvent
from app.logic.handlers.transform.base import ImageTransformEventHandler


class CropImageAndSendToChatEventHandler(
    ImageTransformEventHandler[CropImageAndSendToChatEvent]
):
    async def __call__(self, event: CropImageAndSendToChatEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            width=PositiveNumber(event.old_width),
            height=PositiveNumber(event.old_height),
            name=ImageName(event.name),
        )

        await self._scheduler.schedule_task(
            name=self.__class__,
            schemas=PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class RotateImageAndSendToChatEventHandler(
    ImageTransformEventHandler[RotateImageAndSendToChatEvent]
):
    async def __call__(self, event: RotateImageAndSendToChatEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            width=PositiveNumber(event.width),
            height=PositiveNumber(event.height),
            name=ImageName(event.name),
        )

        await self._scheduler.schedule_task(
            name=self.__class__,
            schemas=PhotoForRotationSchema.from_(entity=image_entity, chat_id=event.chat_id, angle=event.angle),
        )
