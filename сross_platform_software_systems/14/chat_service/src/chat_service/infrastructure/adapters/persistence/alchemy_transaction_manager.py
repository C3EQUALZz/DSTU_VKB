import logging
from typing import Final, override

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.infrastructure.adapters.persistence.constants import (
    DB_COMMIT_DONE,
    DB_CONFLICT,
    DB_CONSTRAINT_VIOLATION,
    DB_FLUSH_DONE,
    DB_FLUSH_FAILED,
    DB_QUERY_FAILED,
    DB_ROLLBACK_DONE,
    DB_ROLLBACK_FAILED,
)
from chat_service.infrastructure.errors.transaction_manager import EntityAddError, RepoError, RollbackError

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SqlAlchemyTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def commit(self) -> None:
        try:
            await self._session.commit()
            logger.debug("%s Main session.", DB_COMMIT_DONE)
        except IntegrityError as e:
            logger.exception(DB_CONSTRAINT_VIOLATION)
            await self.rollback()
            raise EntityAddError(DB_CONSTRAINT_VIOLATION) from e
        except SQLAlchemyError as e:
            logger.exception(DB_CONFLICT)
            await self.rollback()
            raise RepoError(DB_QUERY_FAILED) from e

    @override
    async def rollback(self) -> None:
        try:
            await self._session.rollback()
            logger.debug(DB_ROLLBACK_DONE)
        except SQLAlchemyError as e:
            logger.exception(DB_ROLLBACK_FAILED)
            raise RollbackError(DB_ROLLBACK_FAILED) from e

    @override
    async def flush(self) -> None:
        try:
            await self._session.flush()
            logger.debug("%s Main session.", DB_FLUSH_DONE)
        except IntegrityError as e:
            logger.exception("%s: %s", DB_FLUSH_FAILED, DB_CONSTRAINT_VIOLATION)
            raise EntityAddError(DB_CONSTRAINT_VIOLATION) from e
        except SQLAlchemyError as e:
            raise RepoError(DB_FLUSH_FAILED) from e