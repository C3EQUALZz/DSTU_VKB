from typing import TypeVar

from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)

ET = TypeVar("ET", bound=AbstractEvent)
CT = TypeVar("CT", bound=AbstractCommand)

CommandHandlerMapping = dict[type[AbstractCommand], type[AbstractCommandHandler[AbstractCommand]]]
EventHandlerMapping = dict[type[AbstractEvent], list[type[AbstractEventHandler[AbstractEvent]]]]
