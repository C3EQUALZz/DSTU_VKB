from queue import Queue
from typing import (
    Any,
    Union,
    Final
)

from app.infrastructure.services.idempotency import IdempotencyService
from app.logic.commands.base import BaseCommand
from app.logic.handlers.base import (
    BaseCommandHandler,
    BaseEventHandler,
)

from app.exceptions.logic import MessageBusMessageError
from app.logic.event_buffer import EventBuffer
from app.logic.events.base import BaseEvent


class MessageBus:
    def __init__(
            self,
            event_buffer: EventBuffer,
            idempotency_service: IdempotencyService,
            event_handlers: dict[type[BaseEvent], list[BaseEventHandler[BaseEvent]]],
            command_handlers: dict[type[BaseCommand], BaseCommandHandler[BaseCommand]],
    ) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._queue: Queue[Union[BaseEvent, BaseCommand]] = Queue()
        self._idempotency_service: Final[IdempotencyService] = idempotency_service
        self._command_result: Any = None

    async def handle(self, message: Union[BaseEvent, BaseCommand]) -> None:
        self._queue.put(message)
        while not self._queue.empty():
            message = self._queue.get()
            if self._idempotency_service.is_processed(message):
                continue
            elif isinstance(message, BaseEvent):
                await self._handle_event(event=message)
            elif isinstance(message, BaseCommand):
                await self._handle_command(command=message)
            else:
                raise MessageBusMessageError(
                    "Please configure BootStrap for injection in IoC, there are missing some commands or events"
                )

    async def _handle_event(self, event: BaseEvent) -> None:
        for handler in self._event_handlers[type(event)]:
            await handler(event)
            for event in self._event_buffer.get_events():
                self._queue.put_nowait(event)

    async def _handle_command(self, command: BaseCommand) -> None:
        handler: BaseCommandHandler[BaseCommand] = self._command_handlers[type(command)]
        self._command_result = await handler(command)
        for event in self._event_buffer.get_events():
            self._queue.put_nowait(event)

    @property
    def command_result(self) -> Any:
        return self._command_result
