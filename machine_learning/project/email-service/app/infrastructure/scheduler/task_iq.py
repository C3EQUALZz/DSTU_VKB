from typing import ParamSpec, TypeVar, Mapping, override, Awaitable

from pydantic import BaseModel
from taskiq import AsyncTaskiqDecoratedTask
from typing import Final
from app.exceptions.infrastructure import UnregisteredJobError
from app.infrastructure.scheduler.base import BaseScheduler
from app.logic.handlers.base import AbstractEventHandler
from app.logic.types.handlers import ET

_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")
_EventHandlerTaskIqMapping = Mapping[
    type[AbstractEventHandler[ET]],
    AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType]
]


class TaskIqScheduler(BaseScheduler):
    def __init__(self, task_name_and_func: _EventHandlerTaskIqMapping) -> None:
        self.task_name_and_func: Final[_EventHandlerTaskIqMapping] = task_name_and_func

    @override
    async def schedule_task(self, name: type[AbstractEventHandler[ET]], schemas: BaseModel) -> Awaitable[_ReturnType]:
        result: AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType] | None = self.task_name_and_func.get(name)

        if result is None:
            raise UnregisteredJobError(message=f"Task '{name.__class__.__name__}' is not registered")

        return await result.kiq(schemas)
