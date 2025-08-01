from abc import abstractmethod
from typing import Protocol


class TransactionManager(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...
