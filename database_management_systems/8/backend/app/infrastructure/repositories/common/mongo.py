from abc import ABC
from typing import Dict, Any, Optional
from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
)


class MotorAbstractRepository(ABC):
    def __init__(
        self,
        collection: AsyncIOMotorCollection[Dict[str, Any]],
        session: Optional[AsyncIOMotorClientSession],
    ) -> None:
        self._collection = collection
        self._session = session
