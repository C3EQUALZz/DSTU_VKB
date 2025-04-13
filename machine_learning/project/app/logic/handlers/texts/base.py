from abc import ABC

from app.infrastructure.services.text import TextMessageService
from app.infrastructure.uow.users.base import UsersUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class TextsEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow


class TextsCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork, llm_service: TextMessageService) -> None:
        self._uow: UsersUnitOfWork = uow
        self._llm: TextMessageService = llm_service
