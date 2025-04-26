import inspect
from typing import (
    Any,
    Optional,
    TYPE_CHECKING,
    Union,
)

from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.message_bus import MessageBus
from app.logic.types.handlers import (
    CommandHandlerMapping,
    EventHandlerMapping,
)


if TYPE_CHECKING:
    from types import MappingProxyType

    from app.logic.commands.base import AbstractCommand
    from app.logic.events.base import AbstractEvent


class Bootstrap:
    """
    Bootstrap class for Dependencies Injection purposes.
    """

    def __init__(
        self,
        event_buffer: EventBuffer,
        events_handlers_for_injection: EventHandlerMapping,  # type: ignore
        commands_handlers_for_injection: CommandHandlerMapping,  # type: ignore
        dependencies: Optional[dict[str, Any]] = None,
    ) -> None:
        self._event_buffer = event_buffer
        self._dependencies: dict[str, Any] = {"event_buffer": self._event_buffer}
        self._events_handlers_for_injection = events_handlers_for_injection
        self._commands_handlers_for_injection = commands_handlers_for_injection

        if dependencies:
            self._dependencies.update(dependencies)

    async def get_messagebus(self) -> MessageBus:
        """
        Makes necessary injections to commands handlers and events handlers for creating appropriate messagebus,
        after which returns messagebus instance.
        """

        injected_event_handlers: dict[type[AbstractEvent], list[AbstractEventHandler[AbstractEvent]]] = {
            event_type: [await self._inject_dependencies(handler=handler) for handler in event_handlers]
            for event_type, event_handlers in self._events_handlers_for_injection.items()
        }

        injected_command_handlers: dict[type[AbstractCommand], AbstractCommandHandler[AbstractCommand]] = {
            command_type: await self._inject_dependencies(handler=handler)
            for command_type, handler in self._commands_handlers_for_injection.items()
        }

        return MessageBus(
            event_buffer=self._event_buffer,
            event_handlers=injected_event_handlers,
            command_handlers=injected_command_handlers,
        )

    async def _inject_dependencies(
        self, handler: Union[type[AbstractEventHandler], type[AbstractCommandHandler]]
    ) -> Union[AbstractEventHandler, AbstractCommandHandler]:
        """
        Inspecting handler to know its signature and init params, after which only necessary dependencies will be
        injected to the handler.
        """

        params: MappingProxyType[str, inspect.Parameter] = inspect.signature(handler).parameters
        handler_dependencies: dict[str, Any] = {
            name: dependency for name, dependency in self._dependencies.items() if name in params
        }
        return handler(**handler_dependencies)
