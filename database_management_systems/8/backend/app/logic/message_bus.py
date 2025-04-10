from queue import Queue
from typing import Any, Dict, List, Type, Union

from app.exceptions.logic import MessageBusMessageException
from app.infrastructure.uow.base import AbstractUnitOfWork
from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import (AbstractCommandHandler,
                                     AbstractEventHandler)


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler[AbstractEvent]]],
        command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler[AbstractCommand]],
    ) -> None:
        self._uow = uow
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._queue: Queue[Union[AbstractEvent, AbstractCommand]] = Queue()
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

    async def _handle_event(self, event: AbstractEvent) -> None:
        for handler in self._event_handlers[type(event)]:
            await handler(event)
            for event in self._uow.get_events():
                self._queue.put_nowait(event)

    async def _handle_command(self, command: AbstractCommand) -> None:
        handler: AbstractCommandHandler[AbstractCommand] = self._command_handlers[type(command)]
        self._command_result = await handler(command)
        for event in self._uow.get_events():
            self._queue.put_nowait(event)

    @property
    def command_result(self) -> Any:
        return self._command_result
