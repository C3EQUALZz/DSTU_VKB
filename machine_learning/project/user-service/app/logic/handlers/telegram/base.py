from abc import ABC
from typing import Final

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import EventHandlerTopicFactory
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import AbstractCommandHandler, AbstractEventHandler
from app.logic.types.handlers import CT, ET


class UsersTelegramEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            broker: BaseMessageBroker,
            event_handler_and_topic_factory: EventHandlerTopicFactory,
            users_uow: UsersUnitOfWork,
    ) -> None:
        self._event_buffer: Final[EventBuffer] = event_buffer
        self._broker: Final[BaseMessageBroker] = broker
        self._factory: Final[EventHandlerTopicFactory] = event_handler_and_topic_factory
        self._users_uow: Final[UsersUnitOfWork] = users_uow


class UsersTelegramCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(
            self,
            users_uow: UsersUnitOfWork,
            event_buffer: EventBuffer,
    ) -> None:
        self._uow: Final[UsersUnitOfWork] = users_uow
        self._event_buffer: Final[EventBuffer] = event_buffer
