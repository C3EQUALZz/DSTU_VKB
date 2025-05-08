from abc import ABC
from typing import Final
from app.infrastructure.brokers.factories import EventHandlerTopicFactory

from app.infrastructure.brokers.publishers.kafka.base import BaseKafkaPublisher
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import BaseCommandHandler, BaseEventHandler
from app.logic.types.handlers import CT, ET


class UsersEventHandler(BaseEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            users_uow: UsersUnitOfWork,
            broker: BaseKafkaPublisher,
            event_handler_and_topic_factory: EventHandlerTopicFactory
    ) -> None:
        self._event_buffer: Final[EventBuffer] = event_buffer
        self._users_uow: Final[UsersUnitOfWork] = users_uow
        self._broker: Final[BaseKafkaPublisher] = broker
        self._factory: Final[EventHandlerTopicFactory] = event_handler_and_topic_factory


class UsersCommandHandler(BaseCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            users_uow: UsersUnitOfWork
    ) -> None:
        self._event_buffer: Final[EventBuffer] = event_buffer
        self._users_uow: Final[UsersUnitOfWork] = users_uow
