from abc import ABC

from app.infrastructure.services.user import UsersService
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class UsersEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, event_buffer: EventBuffer) -> None:
        self._event_buffer: EventBuffer = event_buffer


class UsersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, event_buffer: EventBuffer, user_service: UsersService) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._user_service: UsersService = user_service
