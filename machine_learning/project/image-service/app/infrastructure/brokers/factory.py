from typing import Mapping

from app.exceptions.infrastructure import TopicNotFoundInFactoryError
from app.logic.handlers.base import AbstractEventHandler


class EventHandlerTopicFactory:
    def __init__(self, mapping: Mapping[type[AbstractEventHandler], str]) -> None:
        self._mapping: Mapping[type[AbstractEventHandler], str] = mapping

    def get_topic(self, event_handler: type[AbstractEventHandler]) -> str:
        if result := self._mapping.get(event_handler):
            return result

        raise TopicNotFoundInFactoryError("Please add topic for this event handler")


class TaskTopicFactory:
    def __init__(self, mapping: Mapping[str, str]) -> None:
        self._mapping: Mapping[str, str] = mapping

    def get_topic(self, job_name: str) -> str:
        if result := self._mapping.get(job_name):
            return result

        raise TopicNotFoundInFactoryError("Please add topic for this job")
