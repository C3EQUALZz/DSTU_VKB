import logging
from typing import Final

from dishka import FromDishka
from faststream import AckPolicy
from faststream.rabbit import RabbitRouter, RabbitQueue, RabbitMessage
from faststream.rabbit.subscriber import RabbitSubscriber

from chat_service.application.commands.user.delete_user_by_id import (
    DeleteUserByIDCommandHandler,
    DeleteUserByIDCommand
)
from chat_service.presentation.rabbitmq.user.common import USER_EXCHANGE
from chat_service.presentation.rabbitmq.user.delete_user_by_id.schemas import DeleteUserByIDSchemaRequest

delete_user_router: Final[RabbitRouter] = RabbitRouter()

delete_user_queue: Final[RabbitQueue] = RabbitQueue(
    "delete_user_queue",
    auto_delete=True,
    routing_key="user.deleted",
)

delete_user_subscriber: Final[RabbitSubscriber] = delete_user_router.subscriber(
    queue=delete_user_queue,
    exchange=USER_EXCHANGE,
    ack_policy=AckPolicy.REJECT_ON_ERROR
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@delete_user_subscriber
async def delete_user_by_id_handler(
        schema_request: DeleteUserByIDSchemaRequest,
        msg: RabbitMessage,
        interactor: FromDishka[DeleteUserByIDCommandHandler]
) -> None:
    logger.info("Started processing create user handler, message: %s", msg)

    command: DeleteUserByIDCommand = DeleteUserByIDCommand(
        user_id=schema_request.user_id,
    )

    await interactor(command)

    logger.info(
        "Finished processing create user handler, message: %s",
        msg
    )
