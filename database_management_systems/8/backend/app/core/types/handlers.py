from typing import Type, Dict, List, TypeVar

from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler, AbstractHandler,
)

ET = TypeVar("ET", bound=AbstractEvent)
CT = TypeVar("CT", bound=AbstractCommand)
HT = TypeVar("HT", bound=AbstractHandler)

CommandHandlerMapping = Dict[Type[CT], Type[AbstractCommandHandler[CT]]]
EventHandlerMapping = Dict[Type[ET], List[Type[AbstractEventHandler[ET]]]]
