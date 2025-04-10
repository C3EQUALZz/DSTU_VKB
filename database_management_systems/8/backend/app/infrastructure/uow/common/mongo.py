from traceback import TracebackException
from typing import Any, Optional, Self, Type

from app.infrastructure.uow.base import AbstractUnitOfWork
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorClientSession,
                                 AsyncIOMotorDatabase)


class MotorAbstractUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for MongoDB using Motor with transaction support.
    """

    def __init__(self, client: AsyncIOMotorClient[Any], database_name: str) -> None:
        super().__init__()
        self._client = client
        self._database_name = database_name

        self._database: Optional[AsyncIOMotorDatabase[Any]] = None
        self._session: Optional[AsyncIOMotorClientSession] = None

    async def __aenter__(self) -> Self:
        """
        Initializes the database and starts a session for transactions.
        """
        self._database = self._client[self._database_name]
        self._session = await self._client.start_session()
        self._session.start_transaction()
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackException],
    ) -> None:
        """
        Commits or aborts the transaction based on whether an exception occurred.
        """
        if self._session and bool(self._session.in_transaction):
            await super().__aexit__(exc_type, exc_value, traceback)

        if self._session is not None:
            await self._session.end_session()

    async def commit(self) -> None:
        """
        Commits the transaction.
        """
        if self._session and bool(self._session.in_transaction):
            await self._session.commit_transaction()

    async def rollback(self) -> None:
        """
        Aborts the transaction.
        """
        if self._session and bool(self._session.in_transaction):
            await self._session.abort_transaction()
