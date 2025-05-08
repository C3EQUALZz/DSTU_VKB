from typing import Self

from app.infrastructure.repositories.database.users.alchemy import SQLAlchemyUsersRepository
from app.infrastructure.repositories.database.users.base import UsersRepository
from app.infrastructure.uow.alchemy import SQLAlchemyBaseUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


class SQLAlchemyUsersUnitOfWork(SQLAlchemyBaseUnitOfWork, UsersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = SQLAlchemyUsersRepository(session=self._session)
        return uow
