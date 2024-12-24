from typing import Self

from app.infrastructure.repositories.users.base import UsersRepository
from app.infrastructure.repositories.users.mongo import MotorUserRepository
from app.infrastructure.uow.common.mongo import MotorAbstractUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


class MotorUsersUnitOfWork(MotorAbstractUnitOfWork, UsersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = MotorUserRepository(collection=self._database['users'], session=self._session)
        return uow
