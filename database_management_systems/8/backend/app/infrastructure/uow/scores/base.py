from abc import ABC

from app.infrastructure.repositories.scores.base import ScoresRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class ScoresUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with users, that is used by service layer of users module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    scores: ScoresRepository
