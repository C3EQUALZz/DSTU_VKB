from typing import (
    Awaitable,
    Mapping,
    override,
    ParamSpec,
    TypeVar,
)

from pydantic import BaseModel
from taskiq import AsyncTaskiqDecoratedTask

from app.exceptions.infrastructure import UnregisteredTaskError
from app.infrastructure.scheduler.base import BaseScheduler
from app.settings.configs.enums import TaskNamesConfig


_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")


class TaskIqScheduler(BaseScheduler):
    def __init__(self, task_mapping: Mapping[TaskNamesConfig, str]) -> None:
        self._task_mapping: Mapping[TaskNamesConfig, str] = task_mapping

    @override
    async def schedule_task(self, name: TaskNamesConfig, schemas: BaseModel) -> Awaitable[_ReturnType]:
        result: AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType] | None = self._task_mapping.get(name)

        if result is None:
            raise UnregisteredTaskError(message=f"Task '{name.__class__.__name__}' is not registered")

        return await result.kiq(schemas)
