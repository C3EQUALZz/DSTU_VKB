from abc import ABC

from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
)

from app.logic.types.handlers import (CT)


class FileStatsCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork) -> None:
        self._uow: CompressionUnitOfWork = uow
