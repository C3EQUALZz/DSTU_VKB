from abc import ABC, abstractmethod


class BaseDatabaseCLIService(ABC):
    """
    Interface for database CLI service. This was created because there are exists a lot of databases.
    """

    @abstractmethod
    def list_all_databases(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_backup(self) -> None:
        raise NotImplementedError
