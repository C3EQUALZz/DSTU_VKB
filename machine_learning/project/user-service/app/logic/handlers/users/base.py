from abc import ABC

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import EventHandlerTopicFactory
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.handlers.base import AbstractCommandHandler, AbstractEventHandler
from app.logic.types.handlers import CT, ET


class UsersEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            uow: UsersUnitOfWork,
            broker: BaseMessageBroker,
            event_handler_and_topic_factory: EventHandlerTopicFactory
    ) -> None:
        self._uow: UsersUnitOfWork = uow
        self._broker: BaseMessageBroker = broker
        self._factory: EventHandlerTopicFactory = event_handler_and_topic_factory


class UsersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow
