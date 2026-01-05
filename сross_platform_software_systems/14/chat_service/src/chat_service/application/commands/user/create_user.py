import logging
from dataclasses import dataclass
from typing import final, Final
from uuid import UUID

from chat_service.application.common.ports.event_bus import EventBus
from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.ports.user.user_command_gateway import UserCommandGateway
from chat_service.application.common.views.user.create_user_view import CreateUserView
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.services.user_service import UserService
from chat_service.domain.user.values.open_router_api_key import OpenRouterAPIKey
from chat_service.domain.user.values.user_id import UserID
from chat_service.domain.user.values.user_name import UserName

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserCommand:
    user_id: UUID
    user_name: str
    openrouter_api_key: str | None = None


@final
class CreateUserCommandHandler:
    def __init__(
            self,
            user_command_gateway: UserCommandGateway,
            user_service: UserService,
            transaction_manager: TransactionManager,
            event_bus: EventBus
    ) -> None:
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._user_service: Final[UserService] = user_service
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._event_bus: Final[EventBus] = event_bus

    async def __call__(self, data: CreateUserCommand) -> CreateUserView:
        logger.info("Started creating new user with id: %s", data.user_id)

        user_id: UserID = UserID(data.user_id)
        user_name: UserName = UserName(data.user_name)

        new_user: User

        if data.openrouter_api_key is None:
            logger.info("Open router api key is None, user with id: %s has empty key", user_id)
            new_user = self._user_service.create(
                user_id=user_id,
                name=user_name,
            )
        else:
            logger.info("Open router api key is provided for user with id: %s", user_id)
            new_user = self._user_service.create(
                user_id=user_id,
                name=user_name,
                openrouter_api_key=OpenRouterAPIKey(data.openrouter_api_key),
            )

        logger.info("Started saving user with id: %s in persistence storage", user_id)
        await self._user_command_gateway.add(user=new_user)
        logger.info("Started publishing events")
        await self._event_bus.publish(self._user_service.pull_events())
        logger.info("Started commiting transaction")
        await self._transaction_manager.commit()

        logger.info(
            "User with id: %s was successfully created",
            user_id
        )

        return CreateUserView(user_id=user_id)


