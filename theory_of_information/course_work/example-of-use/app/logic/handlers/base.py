from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Generic,
    TypeVar,
)

from app.infrastructure.uow.base import AbstractUnitOfWork
from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent

ET = TypeVar("ET", bound=AbstractEvent)
CT = TypeVar("CT", bound=AbstractCommand)


class AbstractEventHandler(ABC, Generic[ET]):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, event: ET) -> None:
        raise NotImplementedError


class AbstractCommandHandler(ABC, Generic[CT]):
    """
    Abstract command handler class, from which every command handler should be inherited from.
    """

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, command: CT) -> Any:
        raise NotImplementedError
