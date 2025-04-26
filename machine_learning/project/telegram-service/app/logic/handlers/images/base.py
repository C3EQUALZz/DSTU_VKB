from abc import ABC

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import CommandHandlerTopicFactory
from app.infrastructure.scheduler.base import BaseScheduler
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class ImagesEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, event_buffer: EventBuffer, scheduler: BaseScheduler) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._scheduler: BaseScheduler = scheduler


class ImagesCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            broker: BaseMessageBroker,
            topic_command_handler_factory: CommandHandlerTopicFactory
    ) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._broker: BaseMessageBroker = broker
        self._topic_command_handler_factory: CommandHandlerTopicFactory = topic_command_handler_factory
