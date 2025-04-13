from app.application.jobs.images import colorize_photo
from app.domain.entities.message import ImageMessageEntity
from app.logic.commands.images import ColorizeImageCommand
from app.logic.handlers.images.base import ImagesCommandHandler


class ColorizeImageCommandHandler(ImagesCommandHandler[ColorizeImageCommand]):
    async def __call__(self, command: ColorizeImageCommand) -> None:
        image_entity: ImageMessageEntity = ImageMessageEntity(photo=command.data, chat_id=command.chat_id)
        await colorize_photo.kiq(service=self._image_service, image_entity=image_entity)