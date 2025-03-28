from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass(eq=False)
class BaseAppException(Exception, ABC):
    @property
    def message(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def headers(self) -> dict[str, str] | None:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.message
