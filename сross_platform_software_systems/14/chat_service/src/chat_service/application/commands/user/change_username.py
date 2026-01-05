import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.ports.user.user_command_gateway import UserCommandGateway
from chat_service.application.common.ports.user.user_query_gateway import UserQueryGateway
from chat_service.application.errors.user import UserNotFoundError
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.services.user_service import UserService
from chat_service.domain.user.values.user_id import UserID
from chat_service.domain.user.values.user_name import UserName

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeUserNameCommand:
    user_id: UUID
    new_username: str


@final
class ChangeUserNameCommandHandler:
    def __init__(
            self,
            user_command_gateway: UserCommandGateway,
            user_query_gateway: UserQueryGateway,
            transaction_manager: TransactionManager,
            user_service: UserService,
    ) -> None:
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_service: Final[UserService] = user_service

    async def __call__(self, data: ChangeUserNameCommand) -> None:
        logger.info(
            "Started changing username for user with id: %s on new username: %s",
            data.user_id,
            data.new_username
        )

        logger.info("Started validating user id: %s", data.user_id)
        user_id: UserID = UserID(data.user_id)
        logger.info("Started validating user name: %s", data.new_username)
        username: UserName = UserName(data.new_username)

        logger.info("Started checking in query gateway that user exists with id: %s", data.user_id)
        existing_user: User | None = await self._user_query_gateway.read_user_by_id(
            user_id=user_id
        )

        if existing_user is None:
            msg = f"User with id {data.user_id} was not found."
            raise UserNotFoundError(msg)

        logger.info("User with id: %s was found in persistence storage", user_id)

        logger.info(
            "Started requesting domain service for update username: %s for user with id: %s",
            data.new_username,
            data.user_id
        )

        self._user_service.change_user_name(
            user=existing_user,
            new_name=username
        )

        logger.info(
            "Updated username %s in domain service for user with id: %s",
            data.new_username,
            data.user_id
        )

        logger.info("Requesting persistence storage for update user with id: %s", data.user_id)
        await self._user_command_gateway.update(user=existing_user)

        logger.info("Started committing")
        await self._transaction_manager.commit()
