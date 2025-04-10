from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(eq=False)
class BaseAppError(Exception, ABC):
    message: str

    @property
    @abstractmethod
    def status(self) -> int:
        raise NotImplementedError

    @property
    def headers(self) -> dict[str, str] | None:
        return None

    def __str__(self) -> str:
        return self.message
