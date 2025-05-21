from abc import ABC, abstractmethod
from traceback import TracebackException
from typing import Self, Final

from pymysql import Connection


class AbstractUnitOfWork(ABC):
    """
    Interface for any units of work, which would be used for transaction atomicity, according DDD.
    """

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackException | None,
    ) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError



