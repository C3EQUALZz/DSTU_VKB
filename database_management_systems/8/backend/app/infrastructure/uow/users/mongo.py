import logging
from typing import Self

from app.infrastructure.repositories.users.base import UsersRepository
from app.infrastructure.repositories.users.mongo import MotorUsersRepository
from app.infrastructure.uow.common.mongo import MotorAbstractUnitOfWork
from app.infrastructure.uow.users.base import UsersUnitOfWork


logger = logging.getLogger(__name__)


class MotorUsersUnitOfWork(MotorAbstractUnitOfWork, UsersUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()

        if self._database is None:
            logger.error("Database does not exist")
            raise RuntimeError("Database does not exist")

        self.users: UsersRepository = MotorUsersRepository(
            collection=self._database.get_collection("users"), session=self._session
        )

        return uow
