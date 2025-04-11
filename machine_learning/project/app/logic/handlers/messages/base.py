from abc import ABC

from app.infrastructure.uow.message.base import MessagesUnitOfWork
from app.logic.handlers.base import AbstractCommandHandler, AbstractEventHandler
from app.logic.types.handlers import CT, ET


class MessagesEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: MessagesUnitOfWork) -> None:
        self._uow: MessagesUnitOfWork = uow


class MeetingsCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(
        self,
        uow: MessagesUnitOfWork
    ) -> None:
        self._uow: MessagesUnitOfWork = uow