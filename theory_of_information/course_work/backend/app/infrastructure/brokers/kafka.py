from dataclasses import dataclass
from typing import AsyncIterator, override

import orjson
from aiokafka import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer

from app.infrastructure.brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    @override
    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)

    @override
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    @override
    async def stop_consuming_all(self) -> None:
        self.consumer.unsubscribe()

    @override
    async def stop_consuming(self, topic: str | None = None) -> None:
        current_topics = self.consumer.subscription()
        if topic in current_topics:
            updated_topics = list(current_topics)
            updated_topics.remove(topic)
            self.consumer.subscribe(topics=updated_topics)

    @override
    async def close(self) -> None:
        await self.consumer.stop()
        await self.producer.stop()

    @override
    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()
