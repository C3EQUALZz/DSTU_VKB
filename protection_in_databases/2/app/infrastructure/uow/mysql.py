from traceback import TracebackException
from typing import Final, Self

from pymysql import Connection

from app.infrastructure.uow.base import AbstractUnitOfWork


class PyMySQLAbstractUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for SQLAlchemy, from which should be inherited all other units of work,
    which would be based on SQLAlchemy logics.
    """

    def __init__(self, connection: Connection) -> None:
        super().__init__()
        self._connection: Final[Connection] = connection

    def __enter__(self) -> Self:
        self._connection.begin()
        return super().__enter__()

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackException | None,
    ) -> None:
        super().__exit__(exc_type, exc_value, traceback)
        self._connection.close()

    async def commit(self) -> None:
        self._connection.commit()

    async def rollback(self) -> None:
        """
        Rollbacks all uncommited changes.

        Uses self._session.expunge_all() to avoid sqlalchemy.orm.exc.DetachedInstanceError after session rollback,
        due to the fact that selected object is cached by Session. And self._session.rollback() deletes all Session
        cache, which causes error on Domain model, which is not bound now to the session and can not retrieve
        attributes.

        https://pythonhint.com/post/1123713161982291/how-does-a-sqlalchemy-object-get-detached
        """

        self._connection.rollback()
