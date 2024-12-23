from abc import ABC, abstractmethod


class BaseSecurity(ABC):
    @abstractmethod
    def create_access_token(self, oid: str) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, oid: str) -> str:
        ...

    @abstractmethod
    def verify_token(self, oid: str) -> bool:
        ...
