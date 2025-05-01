import importlib
import logging
from functools import lru_cache
from types import ModuleType
from typing import cast

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from faststream.kafka import KafkaBroker

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import EventHandlerTopicFactory
from app.infrastructure.brokers.publishers.faststream import FastStreamKafkaMessageBroker
from app.infrastructure.integrations.color_to_gray.base import BaseImageColorToCrayScaleConverter
from app.infrastructure.integrations.color_to_gray.impl import Cv2ImageColorToCrayScaleConverter
from app.infrastructure.integrations.crop.base import BaseImageCropConverter
from app.infrastructure.integrations.crop.impl import Cv2ImageCropConverter
from app.infrastructure.integrations.gray_to_color.base import BaseImageGrayScaleToColorConverter
from app.infrastructure.integrations.rotation.base import BaseImageRotationConverter
from app.infrastructure.integrations.rotation.impl import Cv2ImageRotationConverter
from app.infrastructure.scheduler.base import BaseScheduler
from app.infrastructure.scheduler.task_iq import TaskIqScheduler
from app.infrastructure.services.colorization import ImageColorizationService
from app.infrastructure.services.transform import ImageTransformService
from app.logic.bootstrap import Bootstrap
from app.logic.commands.colorization import ConvertColorToGrayScaleCommand, ConvertGrayScaleToColorCommand, \
    ConvertColorToGrayScaleAndSendToChatCommand, ConvertGrayScaleToColorAndSendToChatCommand
from app.logic.commands.transform import CropImageAndSendToChatCommand, RotateImageAndSendToChatCommand, \
    CropImageCommand, RotateImageCommand
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.colorization.commands import ConvertColorToGrayScaleCommandHandler, \
    ConvertGrayScaleToColorCommandHandler, ConvertColorToGrayScaleAndSendToChatCommandHandler, \
    ConvertGrayScaleToColorAndSendToChatCommandHandler
from app.logic.handlers.transform.commands import CropImageAndSendToChatCommandHandler, CropImageCommandHandler, \
    RotateImageAndSendToChatCommandHandler, RotateImageCommandHandler
from app.logic.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.settings.configs.app import (
    Settings,
    get_settings,
)

logger = logging.getLogger(__name__)


class HandlerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_mapping_and_command_handlers(self) -> "CommandHandlerMapping":
        """
        Here you have to link commands and command handlers for future inject in Bootstrap
        """
        return cast(
            "CommandHandlerMapping",
            {
                ConvertColorToGrayScaleCommand: ConvertColorToGrayScaleCommandHandler,
                ConvertGrayScaleToColorCommand: ConvertGrayScaleToColorCommandHandler,
                ConvertColorToGrayScaleAndSendToChatCommand: ConvertColorToGrayScaleAndSendToChatCommandHandler,
                ConvertGrayScaleToColorAndSendToChatCommand: ConvertGrayScaleToColorAndSendToChatCommandHandler,
                CropImageAndSendToChatCommand: CropImageAndSendToChatCommandHandler,
                CropImageCommand: CropImageCommandHandler,
                RotateImageAndSendToChatCommand: RotateImageAndSendToChatCommandHandler,
                RotateImageCommand: RotateImageCommandHandler,
            },
        )

    @provide(scope=Scope.APP)
    async def get_mapping_event_and_event_handlers(self) -> "EventHandlerMapping":
        """
        Here you have to link events and event handlers for future inject in Bootstrap
        """
        return cast(
            "EventHandlerMapping",
            {

            },
        )


class SchedulerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_scheduler(self) -> BaseScheduler:
        colorize_tasks_module: ModuleType = importlib.import_module("app.infrastructure.scheduler.tasks.colorization")
        transformation_tasks_module: ModuleType = importlib.import_module("app.infrastructure.scheduler.tasks.transformation")

        return TaskIqScheduler(task_name_and_func={
            ConvertColorToGrayScaleCommand: colorize_tasks_module.convert_rgb_to_grayscale_task,
            ConvertGrayScaleToColorCommand: colorize_tasks_module.convert_grayscale_to_rgb_task,
            CropImageAndSendToChatCommand: transformation_tasks_module.convert_crop_task,
            RotateImageAndSendToChatCommand: transformation_tasks_module.convert_rotation_task
        })


class ImageColorizationProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_color_to_gray_converter(self) -> BaseImageGrayScaleToColorConverter:
        return ...

    @provide(scope=Scope.APP)
    async def get_gray_to_color_converter(self) -> BaseImageColorToCrayScaleConverter:
        return Cv2ImageColorToCrayScaleConverter()

    @provide(scope=Scope.APP)
    async def get_image_colorization_service(
            self,
            color_to_gray_converter: BaseImageColorToCrayScaleConverter,
            gray_to_color_converter: BaseImageGrayScaleToColorConverter,
    ) -> ImageColorizationService:
        return ImageColorizationService(
            color_to_gray_converter=color_to_gray_converter,
            gray_to_color_converter=gray_to_color_converter,
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_mapping_events_and_topic(self, settings: Settings) -> EventHandlerTopicFactory:
        return EventHandlerTopicFactory(
            mapping={

            }
        )

    @provide(scope=Scope.APP)
    async def get_faststream_broker(self, settings: Settings) -> KafkaBroker:
        return KafkaBroker(settings.broker.url)

    @provide(scope=Scope.APP)
    async def get_producer(
            self,
            settings: Settings,
            broker: KafkaBroker,
    ) -> BaseMessageBroker:
        return FastStreamKafkaMessageBroker(
            broker=broker,
            producers={
                settings.broker.image_color_to_grayscale_topic: broker.publisher(
                    settings.broker.image_color_to_grayscale_topic
                ),

                settings.broker.image_grayscale_to_color_topic: broker.publisher(
                    settings.broker.image_grayscale_to_color_topic
                ),

                settings.broker.image_crop_topic: broker.publisher(settings.broker.image_crop_topic),
                settings.broker.image_rotate_topic: broker.publisher(settings.broker.image_rotate_topic),
            }
        )


class ImageTransformProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_crop_converter(self) -> BaseImageCropConverter:
        return Cv2ImageCropConverter()

    @provide(scope=Scope.APP)
    async def get_rotation_converter(self) -> BaseImageRotationConverter:
        return Cv2ImageRotationConverter()

    @provide(scope=Scope.APP)
    async def get_image_transform_service(
            self,
            crop_converter: BaseImageCropConverter,
            rotation_converter: BaseImageRotationConverter,
    ) -> ImageTransformService:
        return ImageTransformService(
            crop_converter=crop_converter,
            rotation_converter=rotation_converter,
        )


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_event_buffer(self) -> EventBuffer:
        return EventBuffer()

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            event_buffer: EventBuffer,
            image_colorization_service: ImageColorizationService,
            scheduler: BaseScheduler,
            image_transform_service: ImageTransformService,
    ) -> Bootstrap:
        return Bootstrap(
            event_buffer=event_buffer,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={
                "image_colorization_service": image_colorization_service,
                "scheduler": scheduler,
                "image_transform_service": image_transform_service,
            },
        )


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(),
        AppProvider(),
        BrokerProvider(),
        ImageColorizationProvider(),
        ImageTransformProvider(),
        SchedulerProvider(),
        context={Settings: get_settings()}
    )
