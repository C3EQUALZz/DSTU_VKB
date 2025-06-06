from typing import Final

from dishka import FromDishka
from faststream.kafka import KafkaRouter
from faststream.kafka.annotations import KafkaMessage

from app.infrastructure.brokers.consumers.chatbot.schemas import TextToChatBotSchema
from app.logic.bootstrap import Bootstrap
from app.logic.events.texts import SendMessageForLLMFromBrokerEvent
from app.logic.message_bus import MessageBus
from app.settings.config import get_settings, Settings

router: Final[KafkaRouter] = KafkaRouter()
settings: Final[Settings] = get_settings()


@router.subscriber(
    settings.broker.text_chatbot_topic,
    group_id=settings.broker.text_chatbot_group_id,
    auto_commit=False
)
async def handle_text_to_chatbot(
        schemas: TextToChatBotSchema,
        msg: KafkaMessage,
        bootstrap: FromDishka[Bootstrap]
) -> None:
    message_bus: MessageBus = await bootstrap.get_messagebus()

    await message_bus.handle(
        SendMessageForLLMFromBrokerEvent(
            content=schemas.content,
            chat_id=schemas.chat_id,
        )
    )

    await msg.ack()
