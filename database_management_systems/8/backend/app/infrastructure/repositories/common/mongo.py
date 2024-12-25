from abc import ABC
from typing import Dict, Any
from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
)


class MotorAbstractRepository(ABC):
    def __init__(
        self,
        collection: AsyncIOMotorCollection[Dict[str, Any]],
        session: AsyncIOMotorClientSession,
    ) -> None:
        self._collection = collection
        self._session = session
