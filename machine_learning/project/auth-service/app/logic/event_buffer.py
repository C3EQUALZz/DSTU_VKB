from collections import deque
from typing import Generator

from app.logic.events.base import BaseEvent


class EventBuffer:
    """
    Class which is used for saving events for future use.
    """

    def __init__(self) -> None:
        self._buffer: deque[BaseEvent] = deque()

    def add(self, event: BaseEvent) -> None:
        """
        Method which adds a new event to the buffer.
        :param event: any event to add
        :return: nothing
        """
        self._buffer.append(event)

    def get_events(self) -> Generator[BaseEvent, None, None]:
        """
        Generator, that gets all events with FIFO.
        :return: generator of events
        """
        while self._buffer:
            yield self._buffer.popleft()
