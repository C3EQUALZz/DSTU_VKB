from abc import abstractmethod
from typing import Protocol


class TransactionManager(Protocol):
    """
    UoW-compatible interface for committing a business transaction.
    The implementation may be an ORM session, such as SQLAlchemy's.
    For more information, see: https://t.me/advice17/60
    """

    @abstractmethod
    async def commit(self) -> None:
        """
        Save all operations in database.
        :return: Nothing
        """
        ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None:
        """
        Method that rolls back all operations.
        :return: Nothing
        """
        ...
