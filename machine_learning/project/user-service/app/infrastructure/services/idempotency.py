from typing import Final, overload

from app.infrastructure.dtos.cache.commands import CommandCacheDTO
from app.infrastructure.dtos.cache.events import EventCacheDTO
from app.infrastructure.repositories.cache.idempotency.commands.base import BaseIdempotencyCommandCacheRepository
from app.infrastructure.repositories.cache.idempotency.events.base import BaseIdempotencyEventCacheRepository
from app.logic.commands.base import AbstractCommand
from app.logic.event_buffer import EventBuffer
from app.logic.events.base import AbstractEvent
from app.logic.events.errors import CacheErrorEvent


class IdempotencyService:
    def __init__(
            self,
            event_buffer: EventBuffer,
            event_cache: BaseIdempotencyEventCacheRepository,
            command_cache: BaseIdempotencyCommandCacheRepository,
            ttl: int = 100
    ) -> None:
        """
        Class which is used for providing Idem the idempotency service for save events in cache.
        :param event_cache: Cache instance for saving events.
        :param command_cache: Cache instance for saving commands.
        :param ttl: Time to live in Redis cache. Default is 24 hours
        """
        self._event_cache: Final[BaseIdempotencyEventCacheRepository] = event_cache
        self._command_cache: Final[BaseIdempotencyCommandCacheRepository] = command_cache
        self._event_buffer: Final[EventBuffer] = event_buffer
        self._ttl: Final[int] = ttl

    @overload
    async def is_processed(self, command_or_event: AbstractEvent) -> bool:
        ...

    @overload
    async def is_processed(self, command_or_event: AbstractCommand) -> bool:
        ...

    async def is_processed(self, command_or_event: AbstractEvent | AbstractCommand) -> bool:
        """
        Check if event was processed,
        :param command_or_event: id of event for checking.
        :return: True if event was processed, otherwise False
        """
        if isinstance(command_or_event, AbstractEvent):
            return await self._event_cache.exists(command_or_event.oid)
        if isinstance(command_or_event, AbstractCommand):
            return await self._command_cache.exists(command_or_event.oid)
        raise TypeError(f"Uncorrected type for command_or_event: {type(command_or_event)}, please use  inheritors from AbstractEvent or AbstractCommand")

    @overload
    async def mark_processed(self, command_or_event: AbstractCommand) -> None:
        ...

    @overload
    async def mark_processed(self, command_or_event: AbstractEvent) -> None:
        ...

    async def mark_processed(self, command_or_event: AbstractEvent | AbstractCommand) -> None:
        """
        Mark event as processed. If any problems with cache it will be published to topic with cache errors.
        Also, changes would be seen in metrics.
        :param command_or_event: event to mark as processed
        :return: None
        """
        is_saved: bool

        if isinstance(command_or_event, AbstractEvent):
            is_saved = await self._event_cache.set(EventCacheDTO(command_or_event), self._ttl)
        elif isinstance(command_or_event, AbstractCommand):
            is_saved = await self._command_cache.set(CommandCacheDTO(command_or_event), self._ttl)
        else:
            raise TypeError(f"Uncorrected type for command_or_event: {type(command_or_event)}, please use  inheritors from AbstractEvent or AbstractCommand")

        if not is_saved:
            self._event_buffer.add(CacheErrorEvent(command_or_event))
