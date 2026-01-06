import logging
from typing import Final

from dishka import FromDishka
from faststream import AckPolicy
from faststream.rabbit import RabbitRouter, RabbitQueue, RabbitMessage
from faststream.rabbit.subscriber import RabbitSubscriber

from chat_service.application.commands.user.create_user import CreateUserCommandHandler, CreateUserCommand
from chat_service.presentation.rabbitmq.user.common import USER_EXCHANGE
from chat_service.presentation.rabbitmq.user.create_user.schemas import CreateUserSchemaRequest

create_user_router: Final[RabbitRouter] = RabbitRouter()

create_user_queue: Final[RabbitQueue] = RabbitQueue(
    "create_user_queue",
    auto_delete=True,
    routing_key="user.created",
)

create_user_subscriber: Final[RabbitSubscriber] = create_user_router.subscriber(
    queue=create_user_queue,
    exchange=USER_EXCHANGE,
    ack_policy=AckPolicy.REJECT_ON_ERROR
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@create_user_subscriber
async def create_user_handler(
        schema_request: CreateUserSchemaRequest,
        msg: RabbitMessage,
        interactor: FromDishka[CreateUserCommandHandler]
) -> None:
    logger.info("Started processing create user handler, message: %s", msg)

    command: CreateUserCommand = CreateUserCommand(
        user_id=schema_request.user_id,
        user_name=schema_request.user_name,
    )

    await interactor(command)

    logger.info("Finished processing create user handler, message: %s", msg)
