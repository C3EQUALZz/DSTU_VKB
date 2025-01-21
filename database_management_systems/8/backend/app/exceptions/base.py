from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception, ABC):
    @property
    def message(self) -> str:
        return "An application error has occurred"

    @property
    @abstractmethod
    def status(self) -> int: ...

    def __str__(self) -> str:
        return self.message
