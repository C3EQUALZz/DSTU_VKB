from abc import ABC
from typing import Final

from app.infrastructure.brokers.factories import EventHandlerTopicFactory
from app.infrastructure.brokers.publishers.kafka.base import BaseKafkaPublisher
from app.infrastructure.scheduler.base import BaseScheduler
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import BaseCommandHandler, BaseEventHandler
from app.logic.types.handlers import CT, ET


class AuthEventHandler(BaseEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            broker: BaseKafkaPublisher,
            event_handler_and_topic_factory: EventHandlerTopicFactory
    ) -> None:
        self._event_buffer: Final[EventBuffer] = event_buffer
        self._broker: Final[BaseKafkaPublisher] = broker
        self._factory: Final[EventHandlerTopicFactory] = event_handler_and_topic_factory


class AuthCommandHandler(BaseCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            scheduler: BaseScheduler
    ) -> None:
        self._scheduler: Final[BaseScheduler] = scheduler
        self._event_buffer: Final[EventBuffer] = event_buffer
