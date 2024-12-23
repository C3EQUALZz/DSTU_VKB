from queue import Queue
from typing import (
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
)

from app.logic.exceptions import MessageBusMessageException
from app.infrastructure.uow.base import AbstractUnitOfWork
from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
    AbstractHandler,
)

ET = TypeVar("ET", bound=AbstractEvent)
CT = TypeVar("CT", bound=AbstractCommand)
HT = TypeVar("HT", bound=AbstractHandler)


class MessageBus:
    def __init__(
            self,
            uow: AbstractUnitOfWork,
            event_handlers: Dict[Type[ET], List[AbstractEventHandler[ET]]],
            command_handlers: Dict[Type[CT], AbstractCommandHandler[CT]],
    ) -> None:
        self._uow = uow
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._queue: Queue = Queue()
        self._command_result: Any = None

    async def handle(self, message: Union[AbstractEvent, AbstractCommand]) -> None:
        self._queue.put(message)
        while not self._queue.empty():
            message = self._queue.get()
            if isinstance(message, AbstractEvent):
                await self._handle_event(event=message)
            elif isinstance(message, AbstractCommand):
                await self._handle_command(command=message)
            else:
                raise MessageBusMessageException()

    async def _handle_event(self, event: ET) -> None:
        for handler in self._event_handlers[type(event)]:
            await handler(event)
            for event in self._uow.get_events():
                self._queue.put_nowait(event)

    async def _handle_command(self, command: CT) -> None:
        handler: AbstractCommandHandler = self._command_handlers[type(command)]
        self._command_result = await handler(command)
        for event in self._uow.get_events():
            self._queue.put_nowait(event)

    @property
    def command_result(self) -> Any:
        return self._command_result