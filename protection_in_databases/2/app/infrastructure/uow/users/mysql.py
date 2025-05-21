from typing import Self

from app.infrastructure.repositories.database.users.mysql import PyMySQLUsersRepository
from app.infrastructure.uow.mysql import PyMySQLAbstractUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


class PyMySQLUsersUnitOfWork(PyMySQLAbstractUnitOfWork, UsersUnitOfWork):
    def __enter__(self) -> Self:
        uow = super().__enter__()
        self.users = PyMySQLUsersRepository(connection=self._connection)
        return uow
