from app.application.jobs.images.schemas import ColorizePhotoSchema
from app.domain.entities.message import ImageMessageEntity
from app.logic.commands.images import ColorizeImageCommand
from app.logic.handlers.images.base import ImagesCommandHandler


class ColorizeImageCommandHandler(ImagesCommandHandler[ColorizeImageCommand]):
    async def __call__(self, command: ColorizeImageCommand) -> None:
        image_entity: ImageMessageEntity = ImageMessageEntity(photo=command.data, chat_id=command.chat_id)
        await self._factory.get_task(type(command)).kiq(ColorizePhotoSchema.from_entity(image_entity))
