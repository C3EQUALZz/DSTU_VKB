from typing import Self

from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


class SQLAlchemyUsersUnitOfWork(SQLAlchemyAbstractUnitOfWork, UsersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = super().__aenter__()
        ...
        return uow
