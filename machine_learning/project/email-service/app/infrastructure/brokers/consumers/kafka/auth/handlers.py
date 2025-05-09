from typing import Final

from dishka import FromDishka
from faststream import Logger
from faststream.kafka import KafkaRouter, KafkaMessage

from app.infrastructure.brokers.consumers.kafka.auth.schemas import UserSendEmailForVerificationSchema
from app.logic.commands.auth import SendVerificationEmailCommand
from app.logic.message_bus import MessageBus
from app.settings.configs.app import get_settings, Settings

router: Final[KafkaRouter] = KafkaRouter()
settings: Final[Settings] = get_settings()


@router.subscriber(
    settings.broker.user_registered_topic,
    group_id=settings.broker.user_registered_group,
    no_ack=True,
    title="user verification via email",
    description="Kafka handler for user verification via email. It will be start working when user registered for system",
)
async def handle_user_registered(
        schemas: UserSendEmailForVerificationSchema,
        msg: KafkaMessage,
        message_bus: FromDishka[MessageBus],
        logger: Logger,
) -> None:
    logger.info(
        "Getting info for email verification, topic: %s, headers: %s, message_id: %s",
        settings.broker.user_registered_topic,
        msg.headers,
        msg.message_id
    )

    await message_bus.handle(
        SendVerificationEmailCommand(
            command_id=schemas.event_id,
            email=str(schemas.email),
            name=schemas.name,
            surname=schemas.surname,
            url=str(schemas.url),
        )
    )

    await msg.ack()

    logger.info(
        "Successfully sent email for verification, topic: %s, headers: %s, message_id: %s",
        settings.broker.user_registered_topic,
        msg.headers,
        msg.message_id
    )
