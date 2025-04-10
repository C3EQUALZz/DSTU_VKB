from typing import Dict, List, Type, TypeVar

from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import (AbstractCommandHandler,
                                     AbstractEventHandler, AbstractHandler)

ET = TypeVar("ET", bound=AbstractEvent)
CT = TypeVar("CT", bound=AbstractCommand)
HT = TypeVar("HT", bound=AbstractHandler)

CommandHandlerMapping = Dict[
    Type[AbstractCommand], Type[AbstractCommandHandler[AbstractCommand]]
]
EventHandlerMapping = Dict[
    Type[AbstractEvent], List[Type[AbstractEventHandler[AbstractEvent]]]
]
