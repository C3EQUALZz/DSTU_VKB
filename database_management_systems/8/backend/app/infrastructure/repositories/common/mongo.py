from abc import ABC

from motor.core import AgnosticClient, AgnosticCollection


class BaseMongoDBRepository(ABC):
    def __init__(
            self,
            mongo_db_client: AgnosticClient,
            mongo_db_db_name: str,
            mongo_db_collection_name: str
    ) -> None:
        self._mongo_db_client: AgnosticClient = mongo_db_client
        self._mongo_db_db_name: str = mongo_db_db_name
        self._mongo_db_collection_name: str = mongo_db_collection_name

    @property
    def _collection(self) -> AgnosticCollection:
        return self._mongo_db_client[self._mongo_db_db_name][self._mongo_db_collection_name]
