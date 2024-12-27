from abc import ABC

from app.core.types.handlers import (
    CT,
    ET,
)
from app.infrastructure.uow.scores.base import ScoresUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)


class ScoresEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: ScoresUnitOfWork) -> None:
        self._uow: ScoresUnitOfWork = uow


class UsersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: ScoresUnitOfWork) -> None:
        self._uow: ScoresUnitOfWork = uow
