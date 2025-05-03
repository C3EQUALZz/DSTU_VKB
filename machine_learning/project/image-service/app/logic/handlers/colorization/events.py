from app.domain.entities.image import ImageEntity
from app.domain.values.image import PositiveNumber, ImageName
from app.infrastructure.scheduler.tasks.schemas import PhotoForSendToChatSchema, \
    PairOfPhotosForStylizationAndForSendToChatSchema
from app.logic.events.colorization import ConvertColorToGrayScaleAndSendToChatEvent, \
    ConvertGrayScaleToColorAndSendToChatEvent, StylizeAndSendToChatEvent
from app.logic.handlers.colorization.base import ImageColorizationEventHandler


class ConvertColorToGrayScaleAndSendToChatEventHandler(
    ImageColorizationEventHandler[ConvertColorToGrayScaleAndSendToChatEvent]
):
    async def __call__(self, event: ConvertColorToGrayScaleAndSendToChatEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            width=PositiveNumber(event.width),
            height=PositiveNumber(event.height),
            name=ImageName(event.name),
        )

        await self._scheduler.schedule_task(
            self.__class__,
            PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class ConvertGrayScaleToColorAndSendToChatEventHandler(
    ImageColorizationEventHandler[ConvertGrayScaleToColorAndSendToChatEvent]
):
    async def __call__(self, event: ConvertGrayScaleToColorAndSendToChatEvent) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=event.data,
            width=PositiveNumber(event.width),
            height=PositiveNumber(event.height),
            name=ImageName(event.name),
        )

        await self._scheduler.schedule_task(
            self.__class__,
            PhotoForSendToChatSchema.from_(entity=image_entity, chat_id=event.chat_id),
        )


class StylizeAndSendToChatEventHandler(
    ImageColorizationEventHandler[StylizeAndSendToChatEvent],
):
    async def __call__(self, event: StylizeAndSendToChatEvent) -> None:
        original_image_entity: ImageEntity = ImageEntity(
            data=event.original_image_data,
            width=PositiveNumber(event.original_width),
            height=PositiveNumber(event.original_height),
            name=ImageName(event.original_name)
        )

        style_image_entity: ImageEntity = ImageEntity(
            data=event.style_image_data,
            width=PositiveNumber(event.style_width),
            height=PositiveNumber(event.style_height),
            name=ImageName(event.style_name)
        )

        await self._scheduler.schedule_task(
            self.__class__,
            PairOfPhotosForStylizationAndForSendToChatSchema.from_(
                original=original_image_entity,
                style=style_image_entity,
                chat_id=event.chat_id
            ),
        )
