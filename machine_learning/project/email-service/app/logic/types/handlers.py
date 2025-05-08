from typing import Dict, List, Type, TypeVar

from app.logic.commands.base import BaseCommand
from app.logic.events.base import BaseEvent
from app.logic.handlers.base import BaseCommandHandler, BaseEventHandler

ET = TypeVar("ET", bound=BaseEvent)
CT = TypeVar("CT", bound=BaseCommand)

CommandHandlerMapping = Dict[Type[BaseCommand], Type[BaseCommandHandler[BaseCommand]]]
EventHandlerMapping = Dict[Type[BaseEvent], List[Type[BaseEventHandler[BaseEvent]]]]
