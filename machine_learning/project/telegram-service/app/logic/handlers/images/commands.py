from app.domain.entities.message import ImageEntity
from app.infrastructure.brokers.schemas.images import (
    ConvertColorImageToGrayScaleSchema,
    ConvertGrayScaleToColorSchema,
    CropImageSchema,
    MetadataImageSchema,
    RotateImageSchema,
)
from app.logic.commands.images import (
    ConvertColorImageToGrayScaleImageCommand,
    ConvertGrayScaleImageToColorImageCommand,
    CropImageCommand,
    GetMetadataFromImageCommand,
    RotateImageCommand,
)
from app.logic.handlers.images.base import ImagesCommandHandler


class ConvertColorImageToGrayScaleImageCommandHandler(ImagesCommandHandler[ConvertColorImageToGrayScaleImageCommand]):
    async def __call__(self, command: ConvertColorImageToGrayScaleImageCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            height=command.height,
            width=command.width,
            name=command.name,
        )

        topic: str = self._topic_command_handler_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=ConvertColorImageToGrayScaleSchema.from_(entity=image_entity, chat_id=command.chat_id)
        )


class ConvertGrayScaleImageToColorImageCommandHandler(ImagesCommandHandler[ConvertGrayScaleImageToColorImageCommand]):
    async def __call__(self, command: ConvertGrayScaleImageToColorImageCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            height=command.height,
            width=command.width,
            name=command.name,
        )

        topic: str = self._topic_command_handler_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=ConvertGrayScaleToColorSchema.from_(entity=image_entity, chat_id=command.chat_id)
        )


class CropImageCommandHandler(ImagesCommandHandler[CropImageCommand]):
    async def __call__(self, command: CropImageCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            height=command.old_height,
            width=command.old_width,
            name=command.name,
        )

        topic: str = self._topic_command_handler_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=CropImageSchema.from_(
                entity=image_entity,
                chat_id=command.chat_id,
                new_height=command.new_height,
                new_width=command.new_width,
            )
        )


class RotateImageCommandHandler(ImagesCommandHandler[RotateImageCommand]):
    async def __call__(self, command: RotateImageCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            height=command.height,
            width=command.width,
            name=command.name,
        )

        topic: str = self._topic_command_handler_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=RotateImageSchema.from_(entity=image_entity, angle=command.angle, chat_id=command.chat_id)
        )


class GetMetadataFromImageCommandHandler(ImagesCommandHandler[GetMetadataFromImageCommand]):
    async def __call__(self, command: GetMetadataFromImageCommand) -> None:
        image_entity: ImageEntity = ImageEntity(
            data=command.data,
            height=command.height,
            width=command.width,
            name=command.name,
        )

        topic: str = self._topic_command_handler_factory.get_topic(self.__class__)

        await self._broker.send_message(
            topic=topic,
            value=MetadataImageSchema.from_(image_entity, chat_id=command.chat_id)
        )
