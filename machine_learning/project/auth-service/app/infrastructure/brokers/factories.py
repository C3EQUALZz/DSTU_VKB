from typing import Mapping, Final

from app.exceptions.infrastructure import TopicNotFoundInFactoryError
from app.logic.handlers.base import BaseEventHandler


class EventHandlerTopicFactory:
    """
    This factory is used for getting topics which related with this event handler.
    For example, you can send same info into different topics.
    """

    def __init__(self, mapping: Mapping[type[BaseEventHandler], str]) -> None:
        self._mapping: Final[Mapping[type[BaseEventHandler], str]] = mapping

    def get_topic(self, event_handler: type[BaseEventHandler]) -> str:
        if result := self._mapping.get(event_handler):
            return result

        raise TopicNotFoundInFactoryError(f"Please add topic for this event handler: {event_handler}")
