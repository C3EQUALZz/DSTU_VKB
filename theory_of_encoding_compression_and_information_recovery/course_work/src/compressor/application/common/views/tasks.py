from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskView:
    task_id: str
