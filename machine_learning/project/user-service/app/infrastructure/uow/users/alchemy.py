from typing import Self

from app.infrastructure.repositories.database.users.alchemy import SQLAlchemyUsersRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


class SQLAlchemyUsersUnitOfWork(SQLAlchemyAbstractUnitOfWork, UsersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users = SQLAlchemyUsersRepository(session=self._session)
        return uow