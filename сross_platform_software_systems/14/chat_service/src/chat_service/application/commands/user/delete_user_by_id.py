import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.ports.user.user_command_gateway import UserCommandGateway
from chat_service.application.common.ports.user.user_query_gateway import UserQueryGateway
from chat_service.application.errors.user import UserNotFoundError
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.user_id import UserID

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteUserByIDCommand:
    user_id: UUID


@final
class DeleteUserByIDCommandHandler:
    def __init__(
            self,
            user_command_gateway: UserCommandGateway,
            user_query_gateway: UserQueryGateway,
            transaction_manager: TransactionManager,
    ) -> None:
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    async def __call__(self, data: DeleteUserByIDCommand) -> None:
        logger.info("Started deleting user by id: %s", data.user_id)

        user_id: UserID = UserID(data.user_id)

        logger.info("Started searching user with this id in persistence storage: %s", user_id)

        existing_user: User | None = await self._user_query_gateway.read_user_by_id(
            user_id=user_id
        )

        if existing_user is None:
            msg = f"User with id: {data.user_id} was not found"
            raise UserNotFoundError(msg)

        logger.info("User with this id %s already exists", data.user_id)

        await self._user_command_gateway.delete_by_id(user_id=user_id)
        await self._transaction_manager.commit()

        logger.info("Finished deleting user with user id: %s", data.user_id)
