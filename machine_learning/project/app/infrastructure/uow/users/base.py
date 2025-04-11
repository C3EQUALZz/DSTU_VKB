from abc import ABC

from app.infrastructure.uow.base import AbstractUnitOfWork


class UsersUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with messages from user, that is used by service layer of messages module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    ...
