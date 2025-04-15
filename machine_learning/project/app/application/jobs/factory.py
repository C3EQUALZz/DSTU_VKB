from typing import ParamSpec, TypeVar

from taskiq import AsyncTaskiqDecoratedTask

from app.exceptions.application import UnregisteredJobError
from app.logic.commands.base import AbstractCommand

_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")


class JobFactory:
    def __init__(
        self, task_name_and_func: dict[type[AbstractCommand], AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType]]
    ) -> None:
        self.task_name_and_func = task_name_and_func

    def get_task(self, name: type[AbstractCommand]) -> AsyncTaskiqDecoratedTask:
        result: AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType] | None = self.task_name_and_func.get(name)

        if result is None:
            raise UnregisteredJobError(message=f"Task '{name.__class__.__name__}' is not registered")

        return result
