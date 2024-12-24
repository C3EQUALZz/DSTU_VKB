from typing import Self, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorClientSession
from app.infrastructure.uow.base import AbstractUnitOfWork


class MotorAbstractUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for MongoDB using Motor with transaction support.
    """

    def __init__(
            self,
            client: AsyncIOMotorClient,
            database_name: str
    ) -> None:
        super().__init__()
        self._client: AsyncIOMotorClient = client
        self._database_name: str = database_name

        self._database: Optional[AsyncIOMotorDatabase] = None
        self._session: Optional[AsyncIOMotorClientSession] = None

    async def __aenter__(self) -> Self:
        """
        Initializes the database and starts a session for transactions.
        """
        self._database = self._client[self._database_name]
        self._session = await self._client.start_session()
        self._session.start_transaction()
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """
        Commits or aborts the transaction based on whether an exception occurred.
        """
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        await super().__aexit__(exc_type, exc_value, traceback)
        await self._session.end_session()

    async def commit(self) -> None:
        """
        Commits the transaction.
        """
        if self._session:
            await self._session.commit_transaction()

    async def rollback(self) -> None:
        """
        Aborts the transaction.
        """
        if self._session:
            await self._session.abort_transaction()
