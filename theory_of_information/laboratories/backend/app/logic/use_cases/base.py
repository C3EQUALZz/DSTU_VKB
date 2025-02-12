from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app.logic.commands.base import AbstractCommand

CT = TypeVar("CT", bound=AbstractCommand)


class BaseUseCase(ABC, Generic[CT]):
    @abstractmethod
    async def __call__(self, command: CT) -> Any:
        raise NotImplementedError
