from abc import ABC
from typing import Final

from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import AbstractCommandHandler, AbstractEventHandler
from app.logic.types.handlers import CT, ET


class UsersEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
    ) -> None:
        self._event_buffer: Final[EventBuffer] = event_buffer


class UsersCommandHandler(AbstractCommandHandler[CT], ABC):
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
