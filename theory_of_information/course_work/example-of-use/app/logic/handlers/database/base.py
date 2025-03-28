from abc import ABC

from app.infrastructure.compressors.factory import CompressorFactory
from app.infrastructure.database.base import BaseDatabaseCLIService
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class DatabaseCLIEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork) -> None:
        self._uow: CompressionUnitOfWork = uow


class DatabaseCLICommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork, database_cli_service: BaseDatabaseCLIService) -> None:
        self._uow: CompressionUnitOfWork = uow
        self._cli_service: BaseDatabaseCLIService = database_cli_service
