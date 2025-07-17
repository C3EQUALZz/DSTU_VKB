import logging
from typing import Final

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from cryptography_methods.application.common.transaction_manager import TransactionManager
from cryptography_methods.infrastructure.errors.transaction_manager import (
    EntityAddError,
    RepositoryException,
    RollbackException
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class SQLAlchemyTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def commit(self) -> None:
        try:
            await self._session.commit()
            logger.debug("Commit was done by session.")
        except IntegrityError as e:
            logger.error("Conflict when adding an entity.", exc_info=True)
            await self.rollback()
            raise EntityAddError("Conflict when adding an entity.") from e
        except SQLAlchemyError as e:
            await self.rollback()
            raise RepositoryException("Database query failed, commit failed.") from e

    @override
    async def rollback(self) -> None:
        try:
            await self._session.rollback()
            logger.debug("Rollback was done by session.")
        except SQLAlchemyError as e:
            logger.error("Failed to make rollback.", exc_info=True)
            raise RollbackException("Failed to make rollback.") from e

    @override
    async def flush(self) -> None:
        try:
            await self._session.flush()
            logger.debug("Flush was done by session.")
        except IntegrityError as e:
            logger.error("Conflict when adding an entity.", exc_info=True)
            raise EntityAddError("Conflict when adding an entity.") from e
        except SQLAlchemyError as e:
            raise RepositoryException("Database query failed, commit failed.") from e
