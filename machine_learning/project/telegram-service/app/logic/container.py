import importlib
import logging
from functools import lru_cache
from types import ModuleType
from typing import cast, Final

from dishka import (
    AsyncContainer,
    from_context,
    make_async_container,
    provide,
    Provider,
    Scope,
)
from faststream.kafka import KafkaBroker

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import (
    CommandHandlerTopicFactory,
    EventHandlerTopicFactory,
)
from app.infrastructure.brokers.publishers.faststream import FastStreamKafkaMessageBroker
from app.infrastructure.scheduler.base import BaseScheduler
from app.infrastructure.scheduler.task_iq import TaskIqScheduler
from app.logic.bootstrap import Bootstrap
from app.logic.commands.images import (
    ConvertColorImageToGrayScaleImageCommand,
    ConvertGrayScaleImageToColorImageCommand,
    CropImageCommand,
    GetMetadataFromImageCommand,
    RotateImageCommand,
)
from app.logic.commands.texts import SendTextMessageToChatBotCommand
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.logic.event_buffer import EventBuffer
from app.logic.events.images import ConvertedImageFromBrokerEvent
from app.logic.events.user import UserCreateEvent, UserUpdateEvent, UserDeleteEvent
from app.logic.handlers.images.commands import (
    ConvertColorImageToGrayScaleImageCommandHandler,
    ConvertGrayScaleImageToColorImageCommandHandler,
    CropImageCommandHandler,
    GetMetadataFromImageCommandHandler,
    RotateImageCommandHandler,
)
from app.logic.handlers.images.events import ConvertedImageFromBrokerEventHandler
from app.logic.handlers.texts.commands import SendTextMessageToChatBotCommandHandler
from app.logic.handlers.users.commands import CreateUserCommandHandler, DeleteUserCommandHandler
from app.logic.handlers.users.events import UserCreateEventHandler, UserUpdateEventHandler, UserDeleteEventHandler
from app.logic.message_bus import MessageBus
from app.logic.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)
from app.settings.configs.app import (
    get_settings,
    Settings,
)
from app.settings.configs.enums import TaskNamesConfig

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
                SendTextMessageToChatBotCommand: SendTextMessageToChatBotCommandHandler,
                GetMetadataFromImageCommand: GetMetadataFromImageCommandHandler,
                ConvertColorImageToGrayScaleImageCommand: ConvertColorImageToGrayScaleImageCommandHandler,
                ConvertGrayScaleImageToColorImageCommand: ConvertGrayScaleImageToColorImageCommandHandler,
                CropImageCommand: CropImageCommandHandler,
                RotateImageCommand: RotateImageCommandHandler,
                CreateUserCommand: CreateUserCommandHandler,
                UpdateUserCommand: UserUpdateEventHandler,
                DeleteUserCommand: DeleteUserCommandHandler,
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
                ConvertedImageFromBrokerEvent: [ConvertedImageFromBrokerEventHandler],
                UserCreateEvent: [UserCreateEventHandler],
                UserUpdateEvent: [UserUpdateEventHandler],
                UserDeleteEvent: [UserDeleteEventHandler],
            },
        )


class BrokerProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_mapping_events_and_topic(self, settings: Settings) -> EventHandlerTopicFactory:
        return EventHandlerTopicFactory(
            mapping={
                UserCreateEventHandler: settings.broker.user_create_topic,
                UserUpdateEventHandler: settings.broker.user_update_topic,
                UserDeleteEventHandler: settings.broker.user_delete_topic,
            }
        )

    @provide(scope=Scope.APP)
    async def get_faststream_broker(self, settings: Settings) -> KafkaBroker:
        return KafkaBroker(settings.broker.url, logger=logger)

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

class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_event_buffer(self) -> EventBuffer:
        return EventBuffer()

    @provide(scope=Scope.APP)
    async def get_command_handler_topic_factory(self, settings: Settings) -> CommandHandlerTopicFactory:
        return CommandHandlerTopicFactory(
            mapping={
                SendTextMessageToChatBotCommandHandler: settings.broker.text_to_chatbot_topic,
                GetMetadataFromImageCommandHandler: settings.broker.image_metadata_topic,
                ConvertColorImageToGrayScaleImageCommandHandler: settings.broker.image_color_to_grayscale_topic,
                ConvertGrayScaleImageToColorImageCommandHandler: settings.broker.image_grayscale_to_color_topic,
                CropImageCommandHandler: settings.broker.image_crop_topic,
                RotateImageCommandHandler: settings.broker.image_rotate_topic
            }
        )

    @provide(scope=Scope.APP)
    async def get_scheduler(self) -> BaseScheduler:
        images_tasks_module: ModuleType = importlib.import_module("app.infrastructure.scheduler.tasks.images.handlers")

        return TaskIqScheduler(
            task_mapping={
                TaskNamesConfig.SEND_CONVERTED_IMAGE_TO_USER: images_tasks_module.send_converted_image_task,
                TaskNamesConfig.IMAGE_METADATA: images_tasks_module.send_metadata_from_image_task,
            }
        )

    @provide(scope=Scope.APP)
    async def get_bootstrap(
            self,
            events: EventHandlerMapping,
            commands: CommandHandlerMapping,
            event_buffer: EventBuffer,
            scheduler: BaseScheduler,
            broker: BaseMessageBroker,
            topic_command_handler_factory: CommandHandlerTopicFactory,
            event_handler_topic_factory: EventHandlerTopicFactory
    ) -> Bootstrap:
        return Bootstrap(
            event_buffer=event_buffer,
            events_handlers_for_injection=events,
            commands_handlers_for_injection=commands,
            dependencies={
                "scheduler": scheduler,
                "broker": broker,
                "topic_command_handler_factory": topic_command_handler_factory,
                "event_handler_topic_factory": event_handler_topic_factory
            },
        )

    @provide(scope=Scope.APP)
    async def get_message_bus(self, bootstrap: Bootstrap) -> MessageBus:
        return await bootstrap.get_messagebus()


@lru_cache(maxsize=1)
def get_container() -> AsyncContainer:
    return make_async_container(
        HandlerProvider(), AppProvider(), BrokerProvider(), context={Settings: get_settings()}
    )
