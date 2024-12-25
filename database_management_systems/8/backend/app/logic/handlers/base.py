from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Generic,
)

from app.core.types.handlers import (
    CT,
    ET,
)
from app.infrastructure.uow.base import AbstractUnitOfWork


class AbstractHandler(ABC):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError


class AbstractEventHandler(AbstractHandler, ABC, Generic[ET]):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    async def __call__(self, event: ET) -> None:
        raise NotImplementedError


class AbstractCommandHandler(AbstractHandler, ABC, Generic[CT]):
    """
    Abstract command handler class, from which every command handler should be inherited from.
    """

    @abstractmethod
    async def __call__(self, command: CT) -> Any:
        raise NotImplementedError
