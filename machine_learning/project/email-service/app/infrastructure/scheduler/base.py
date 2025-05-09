from abc import ABC, abstractmethod
from typing import TypeVar, Awaitable

from pydantic import BaseModel

from app.logic.handlers.base import AbstractEventHandler
from app.logic.types.handlers import ET

_ReturnType = TypeVar("_ReturnType")


class BaseScheduler(ABC):
    @abstractmethod
    async def schedule_task(self, name: type[AbstractEventHandler[ET]], schemas: BaseModel) -> Awaitable[_ReturnType]:
        raise NotImplementedError
