from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Awaitable,
    TypeVar,
)

from pydantic import BaseModel

from app.settings.configs.enums import TaskNamesConfig


_ReturnType = TypeVar("_ReturnType")


class BaseScheduler(ABC):
    @abstractmethod
    async def schedule_task(self, name: TaskNamesConfig, schemas: BaseModel) -> Awaitable[_ReturnType]:
        raise NotImplementedError
