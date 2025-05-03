import importlib
import logging
from functools import lru_cache
from types import ModuleType
from typing import cast, Final

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
from app.infrastructure.brokers.factory import EventHandlerTopicFactory, TaskTopicFactory
from app.infrastructure.brokers.publishers.faststream import FastStreamKafkaMessageBroker
from app.infrastructure.integrations.color_to_gray.base import BaseImageColorToCrayScaleConverter
from app.infrastructure.integrations.color_to_gray.impl import Cv2ImageColorToCrayScaleConverter
from app.infrastructure.integrations.crop.base import BaseImageCropConverter
from app.infrastructure.integrations.crop.impl import Cv2ImageCropConverter
from app.infrastructure.integrations.gray_to_color.base import BaseImageGrayScaleToColorConverter
from app.infrastructure.integrations.gray_to_color.impl import KerasImageMessageColorizationModel
from app.infrastructure.integrations.rotation.base import BaseImageRotationConverter
from app.infrastructure.integrations.rotation.impl import Cv2ImageRotationConverter
from app.infrastructure.integrations.stylization.base import BaseImageStylizationConverter
from app.infrastructure.integrations.stylization.impl import KerasImageStylizationConverter
from app.infrastructure.scheduler.base import BaseScheduler
from app.infrastructure.scheduler.task_iq import TaskIqScheduler
from app.infrastructure.services.colorization import ImageColorizationService
from app.infrastructure.services.transform import ImageTransformService
from app.logic.bootstrap import Bootstrap
from app.logic.commands.colorization import ConvertColorToGrayScaleCommand, ConvertGrayScaleToColorCommand, \
    StylizeCommand
from app.logic.commands.transform import CropImageCommand, RotateImageCommand
from app.logic.event_buffer import EventBuffer
from app.logic.events.colorization import ConvertColorToGrayScaleAndSendToChatEvent, \
    ConvertGrayScaleToColorAndSendToChatEvent, StylizeAndSendToChatEvent
from app.logic.events.transform import CropImageAndSendToChatEvent, RotateImageAndSendToChatEvent
from app.logic.handlers.colorization.commands import ConvertColorToGrayScaleCommandHandler, \
    ConvertGrayScaleToColorCommandHandler, StylizeCommandHandler
from app.logic.handlers.colorization.events import ConvertColorToGrayScaleAndSendToChatEventHandler, \
    ConvertGrayScaleToColorAndSendToChatEventHandler, StylizeAndSendToChatEventHandler
from app.logic.handlers.transform.commands import CropImageCommandHandler, RotateImageCommandHandler
from app.logic.handlers.transform.events import CropImageAndSendToChatEventHandler, RotateImageAndSendToChatEventHandler
from app.logic.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.settings.configs.app import (
    Settings,
    get_settings,
)
from app.settings.configs.enums import TaskNamesConfig
from app.infrastructure.brokers.consumers.kafka.colorization.handlers import router as colorization_kafka_router
from app.infrastructure.brokers.consumers.kafka.transformation.handlers import router as transformation_kafka_router

logger: Final[logging.Logger] = logging.getLogger(__name__)


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
                CropImageCommand: CropImageCommandHandler,
                RotateImageCommand: RotateImageCommandHandler,
                StylizeCommand: StylizeCommandHandler,
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
                ConvertColorToGrayScaleAndSendToChatEvent: [ConvertColorToGrayScaleAndSendToChatEventHandler],
                ConvertGrayScaleToColorAndSendToChatEvent: [ConvertGrayScaleToColorAndSendToChatEventHandler],
                StylizeAndSendToChatEvent: [StylizeAndSendToChatEventHandler],
                CropImageAndSendToChatEvent: [CropImageAndSendToChatEventHandler],
                RotateImageAndSendToChatEvent: [RotateImageAndSendToChatEventHandler],
            },
        )


class SchedulerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_scheduler(self) -> BaseScheduler:
        colorize_tasks_module: ModuleType = importlib.import_module("app.infrastructure.scheduler.tasks.colorization")
        transformation_tasks_module: ModuleType = importlib.import_module(
            "app.infrastructure.scheduler.tasks.transformation"
        )

        return TaskIqScheduler(task_name_and_func={
            ConvertColorToGrayScaleAndSendToChatEventHandler: colorize_tasks_module.convert_rgb_to_grayscale_task,
            ConvertGrayScaleToColorAndSendToChatEventHandler: colorize_tasks_module.convert_grayscale_to_rgb_task,
            StylizeAndSendToChatEventHandler: colorize_tasks_module.convert_stylization_task,
            CropImageAndSendToChatEventHandler: transformation_tasks_module.convert_crop_task,
            RotateImageAndSendToChatEventHandler: transformation_tasks_module.convert_rotation_task
        })

    @provide(scope=Scope.APP)
    async def get_task_topic_factory(self, settings: Settings) -> TaskTopicFactory:
        return TaskTopicFactory(
            mapping={
                TaskNamesConfig.STYLIZATION: settings.broker.image_style_result_topic,
                TaskNamesConfig.GRAYSCALE_TO_RGB: settings.broker.image_grayscale_to_color_result_topic,
                TaskNamesConfig.RGB_TO_GRAYSCALE: settings.broker.image_color_to_grayscale_result_topic,
                TaskNamesConfig.CROP: settings.broker.image_crop_result_topic,
                TaskNamesConfig.ROTATION: settings.broker.image_rotate_result_topic
            }
        )


class ImageColorizationProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_color_to_gray_converter(self, settings: Settings) -> BaseImageGrayScaleToColorConverter:
        return KerasImageMessageColorizationModel(path_to_model=settings.models.path_to_colorization_model)

    @provide(scope=Scope.APP)
    async def get_gray_to_color_converter(self) -> BaseImageColorToCrayScaleConverter:
        return Cv2ImageColorToCrayScaleConverter()

    @provide(scope=Scope.APP)
    async def get_stylization_converter(self, settings: Settings) -> BaseImageStylizationConverter:
        return KerasImageStylizationConverter(
            path_to_stylization_model=settings.models.path_to_stylization_model
        )

    @provide(scope=Scope.APP)
    async def get_image_colorization_service(
            self,
            color_to_gray_converter: BaseImageColorToCrayScaleConverter,
            gray_to_color_converter: BaseImageGrayScaleToColorConverter,
            stylization_converter: BaseImageStylizationConverter,
    ) -> ImageColorizationService:
        return ImageColorizationService(
            color_to_gray_converter=color_to_gray_converter,
            gray_to_color_converter=gray_to_color_converter,
            stylization_converter=stylization_converter,
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
        broker: KafkaBroker = KafkaBroker(settings.broker.url)
        broker.include_router(colorization_kafka_router)
        broker.include_router(transformation_kafka_router)
        return broker

    @provide(scope=Scope.APP)
    async def get_producer(
            self,
            settings: Settings,
            broker: KafkaBroker,
    ) -> BaseMessageBroker:
        return FastStreamKafkaMessageBroker(
            broker=broker,
            producers={
                settings.broker.image_color_to_grayscale_result_topic: broker.publisher(
                    settings.broker.image_color_to_grayscale_result_topic
                ),

                settings.broker.image_grayscale_to_color_result_topic: broker.publisher(
                    settings.broker.image_grayscale_to_color_result_topic
                ),
                settings.broker.image_crop_result_topic: broker.publisher(settings.broker.image_crop_result_topic),
                settings.broker.image_rotate_result_topic: broker.publisher(settings.broker.image_rotate_result_topic),
                settings.broker.image_style_result_topic: broker.publisher(settings.broker.image_style_result_topic),
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
