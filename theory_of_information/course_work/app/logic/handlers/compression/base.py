from abc import ABC

from app.infrastructure.compressors.factory import CompressorFactory
from app.infrastructure.uow.compression import CompressionUnitOfWork
from app.logic.handlers.base import (AbstractCommandHandler,
                                     AbstractEventHandler)
from app.logic.types.handlers import CT, ET


class CompressionEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork) -> None:
        self._uow: CompressionUnitOfWork = uow


class CompressionCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: CompressionUnitOfWork, factory: CompressorFactory) -> None:
        self._uow: CompressionUnitOfWork = uow
        self._factory: CompressorFactory = factory
