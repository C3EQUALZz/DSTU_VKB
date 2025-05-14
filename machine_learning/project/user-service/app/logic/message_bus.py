from queue import Queue
from typing import (
    Any,
    Union,
    Final
)

from app.infrastructure.services.idempotency import IdempotencyService
from app.logic.commands.base import AbstractCommand
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)

from app.exceptions.logic import MessageBusMessageError
from app.logic.event_buffer import EventBuffer
from app.logic.events.base import AbstractEvent


class MessageBus:
    def __init__(
            self,
            event_buffer: EventBuffer,
            idempotency_service: IdempotencyService,
            event_handlers: dict[type[AbstractEvent], list[AbstractEventHandler[AbstractEvent]]],
            command_handlers: dict[type[AbstractCommand], AbstractCommandHandler[AbstractCommand]],
    ) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._queue: Queue[Union[AbstractEvent, AbstractCommand]] = Queue()
        self._idempotency_service: Final[IdempotencyService] = idempotency_service
        self._command_result: Any = None

    async def handle(self, message: Union[AbstractEvent, AbstractCommand]) -> None:
        self._queue.put(message)
        while not self._queue.empty():
            message = self._queue.get()
            if await self._idempotency_service.is_processed(message):
                continue
            elif isinstance(message, AbstractEvent):
                await self._handle_event(event=message)
            elif isinstance(message, AbstractCommand):
                await self._handle_command(command=message)
            else:
                raise MessageBusMessageError(
                    "Please configure BootStrap for injection in IoC, there are missing some commands or events"
                )

    async def _handle_event(self, event: AbstractEvent) -> None:
        for handler in self._event_handlers[type(event)]:
            await handler(event)
            for event in self._event_buffer.get_events():
                self._queue.put_nowait(event)

    async def _handle_command(self, command: AbstractCommand) -> None:
        handler: AbstractCommandHandler[AbstractCommand] = self._command_handlers[type(command)]
        self._command_result = await handler(command)
        for event in self._event_buffer.get_events():
            self._queue.put_nowait(event)

    @property
    def command_result(self) -> Any:
        return self._command_result
