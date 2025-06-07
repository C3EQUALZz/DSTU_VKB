from abc import ABC

from app.infrastructure.brokers.base import BaseMessageBroker
from app.infrastructure.brokers.factory import EventHandlerTopicFactory
from app.infrastructure.services.text import TextMessageService
from app.logic.event_buffer import EventBuffer
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
)
from app.logic.types.handlers import (
    CT,
    ET,
)


class TextsEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(
            self,
            event_buffer: EventBuffer,
            text_service: TextMessageService,
            factory: EventHandlerTopicFactory,
            broker: BaseMessageBroker
    ) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._text_service: TextMessageService = text_service
        self._broker: BaseMessageBroker = broker
        self._factory: EventHandlerTopicFactory = factory


class TextsCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, event_buffer: EventBuffer, text_service: TextMessageService) -> None:
        self._event_buffer: EventBuffer = event_buffer
        self._text_service: TextMessageService = text_service
