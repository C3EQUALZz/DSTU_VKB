from abc import ABC

from app.infrastructure.repositories.master.base import MasterRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class MasterUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with books, that is used by service layer of books module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    master: MasterRepository
