from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.infrastructure.brokers.publishers.base import BasePublisher


class BaseKafkaPublisher(BasePublisher, ABC):
    @abstractmethod
    async def send_message(self, topic: str, value: BaseModel) -> None:
        raise NotImplementedError
