from abc import ABC, abstractmethod
from typing import TypeVar, Awaitable

from pydantic import BaseModel

from app.logic.commands.base import AbstractCommand

_ReturnType = TypeVar("_ReturnType")


class BaseScheduler(ABC):
    @abstractmethod
    async def schedule_task(self, name: type[AbstractCommand], schemas: BaseModel) -> Awaitable[_ReturnType]:
        raise NotImplementedError
