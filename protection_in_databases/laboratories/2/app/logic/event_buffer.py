from collections import deque
from typing import Generator

from app.logic.events.base import AbstractEvent


class EventBuffer:
    def __init__(self) -> None:
        self._buffer: deque[AbstractEvent] = deque()

    def add(self, event: AbstractEvent) -> None:
        self._buffer.append(event)

    def get_events(self) -> Generator[AbstractEvent, None, None]:
        """Генератор, который извлекает события по FIFO."""
        while self._buffer:
            yield self._buffer.popleft()
