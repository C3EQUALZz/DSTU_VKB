import logging
from typing import Self

from app.infrastructure.repositories.scores.base import ScoresRepository
from app.infrastructure.repositories.scores.mongo import MotorScoresRepository
from app.infrastructure.uow.common.mongo import MotorAbstractUnitOfWork
from app.infrastructure.uow.scores.base import ScoresUnitOfWork

logger = logging.getLogger(__name__)


class MotorUsersUnitOfWork(MotorAbstractUnitOfWork, ScoresUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()

        if self._database is None:
            logger.error('Database does not exist')
            raise RuntimeError('Database does not exist')

        self.scores: ScoresRepository = MotorScoresRepository(
            collection=self._database.get_collection("scores"),
            session=self._session
        )

        return uow
