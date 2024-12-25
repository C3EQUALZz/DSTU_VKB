from abc import ABC

from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
)


class MotorAbstractRepository(ABC):
    def __init__(
            self,
            collection: AsyncIOMotorCollection,
            session: AsyncIOMotorClientSession,
    ) -> None:
        self._collection: AsyncIOMotorCollection = collection
        self._session: AsyncIOMotorClientSession = session
