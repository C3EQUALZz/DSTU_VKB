from abc import ABC

from app.infrastructure.repositories.database.base import DatabaseDumpRepository
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class S3EventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork) -> None:
        self._uow: CompressionUnitOfWork = uow


class S3CommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork, s3_dump_repository: DatabaseDumpRepository) -> None:
        self._uow: CompressionUnitOfWork = uow
        self._repository = s3_dump_repository
