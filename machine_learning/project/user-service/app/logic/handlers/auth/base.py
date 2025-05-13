from abc import ABC
from typing import Final
from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.handlers.base import AbstractCommandHandler, AbstractEventHandler
from app.logic.types.handlers import CT, ET


class AuthEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every auth event handler should be inherited from.
    """

    def __init__(self, users_uow: UsersUnitOfWork, broker: BaseMessageBroker) -> None:
        self._users_uow: Final[UsersUnitOfWork] = users_uow
        self._broker: Final[BaseMessageBroker] = broker


class AuthCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every auth command handler should be inherited from.
    """

    def __init__(self, users_uow: UsersUnitOfWork) -> None:
        self._users_uow: Final[UsersUnitOfWork] = users_uow
