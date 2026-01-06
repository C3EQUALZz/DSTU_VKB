import logging
from typing import Final

from dishka import FromDishka
from faststream import AckPolicy
from faststream.rabbit import (
    RabbitRouter,
    RabbitQueue,
    RabbitMessage
)
from faststream.rabbit.subscriber import RabbitSubscriber

from chat_service.application.commands.user.change_username import ChangeUserNameCommandHandler, ChangeUserNameCommand
from chat_service.presentation.rabbitmq.user.change_username.schemas import ChangeUsernameSchemaRequest
from chat_service.presentation.rabbitmq.user.common import USER_EXCHANGE

change_username_router: Final[RabbitRouter] = RabbitRouter()

change_username_queue: Final[RabbitQueue] = RabbitQueue(
    "change_username_queue",
    auto_delete=True,
    routing_key="user.updated.username",
)

change_username_subscriber: Final[RabbitSubscriber] = change_username_router.subscriber(
    queue=change_username_queue,
    exchange=USER_EXCHANGE,
    ack_policy=AckPolicy.REJECT_ON_ERROR
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@change_username_subscriber
async def change_username_handler(
        schema_request: ChangeUsernameSchemaRequest,
        message: RabbitMessage,
        interactor: FromDishka[ChangeUserNameCommandHandler],
) -> None:
    logger.info(
        "Started changing on new username: %s for user with id: %s, rabbit message: %s",
        schema_request.new_username,
        schema_request.user_id,
        message,
    )

    command: ChangeUserNameCommand = ChangeUserNameCommand(
        new_username=schema_request.new_username,
        user_id=schema_request.user_id,
    )

    await interactor(command)

    logger.info(
        "Finished changing on new username: %s for user with id: %s",
        schema_request.new_username,
        schema_request.user_id,
    )
