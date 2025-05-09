from abc import ABC, abstractmethod
from typing import TypeVar, Awaitable, overload

from pydantic import BaseModel

from app.logic.handlers.base import BaseEventHandler, BaseCommandHandler
from app.logic.types.handlers import ET, CT

_ReturnType = TypeVar("_ReturnType")


class BaseScheduler(ABC):
    @overload
    async def schedule_task(self, name: type[BaseEventHandler[ET]], schemas: BaseModel) -> Awaitable[_ReturnType]:
        ...

    @overload
    async def schedule_task(self, name: type[BaseCommandHandler[CT]], schemas: BaseModel) -> Awaitable[_ReturnType]:
        ...

    @abstractmethod
    async def schedule_task(
            self,
            name: type[BaseEventHandler[ET]] | type[BaseCommandHandler[CT]],
            schemas: BaseModel
    ) -> Awaitable[_ReturnType]:
        raise NotImplementedError
