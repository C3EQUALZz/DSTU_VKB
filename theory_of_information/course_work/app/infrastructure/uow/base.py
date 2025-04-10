from abc import ABC, abstractmethod
from collections.abc import Generator
from traceback import TracebackException
from typing import Self

from app.logic.events.base import AbstractEvent


class AbstractUnitOfWork(ABC):
    """
    Interface for any units of work, which would be used for transaction atomicity, according DDD.
    """

    def __init__(self) -> None:
        self._events: list[AbstractEvent] = []

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackException | None,
    ) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    def add_event(self, event: AbstractEvent) -> None:
        self._events.append(event)

    def get_events(self) -> Generator[AbstractEvent, None, None]:
        """
        Using generator to get elements only when they needed.
        Also can not use self._events directly, not to run events endlessly.
        """

        while self._events:
            yield self._events.pop(0)
