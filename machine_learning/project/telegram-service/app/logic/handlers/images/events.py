from app.domain.entities.message import ImageEntity
from app.infrastructure.scheduler.tasks.images.schemas import ImageForSendToChatSchema
from app.logic.events.images import ConvertedImageFromBrokerEvent
from app.logic.handlers.images.base import ImagesEventHandler
from app.settings.configs.enums import TaskNamesConfig


class ConvertedImageFromBrokerEventHandler(ImagesEventHandler[ConvertedImageFromBrokerEvent]):
    async def __call__(self, event: ConvertedImageFromBrokerEvent) -> None:
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
