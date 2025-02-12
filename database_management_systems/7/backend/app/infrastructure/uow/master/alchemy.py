from typing import Self

from app.infrastructure.repositories.master.alchemy import SQLAlchemyMasterRepository
from app.infrastructure.repositories.master.base import MasterRepository
from app.infrastructure.uow.base import SQLAlchemyAbstractUnitOfWork
from app.infrastructure.uow.master.base import MasterUnitOfWork


class SQLAlchemyMasterUnitOfWork(SQLAlchemyAbstractUnitOfWork, MasterUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.master: MasterRepository = SQLAlchemyMasterRepository(session=self._session)
        return uow
