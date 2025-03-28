from abc import ABC, abstractmethod

class BaseDatabaseCLIService(ABC):
    @abstractmethod
    def list_all_databases(self) -> None:
        raise NotImplementedError