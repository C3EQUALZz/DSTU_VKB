import logging
from dataclasses import dataclass
from typing import final, Final

from chat_service.application.common.ports.transaction_manager import TransactionManager
from chat_service.application.common.ports.user.user_command_gateway import UserCommandGateway
from chat_service.application.common.services.current_user_service import CurrentUserService
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.services.user_service import UserService
from chat_service.domain.user.values.open_router_api_key import OpenRouterAPIKey

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangeOpenRouterAPIKeyCommand:
    new_openrouter_api_key: str


@final
class ChangeOpenRouterAPIKeyCommandHandler:
    def __init__(
            self,
            user_command_gateway: UserCommandGateway,
            transaction_manager: TransactionManager,
            user_service: UserService,
            current_user_service: CurrentUserService,
    ) -> None:
        self._user_command_gateway: Final[UserCommandGateway] = user_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_service: Final[UserService] = user_service
        self._current_user_service: Final[CurrentUserService] = current_user_service

    async def __call__(self, data: ChangeOpenRouterAPIKeyCommand) -> None:
        current_user: User = await self._current_user_service.get_current_user()

        logger.info(
            "Setting new openrouter API key: %s for user with id: %s",
            current_user.id,
            data.new_openrouter_api_key
        )

        logger.info(
            "Started requesting domain service for changing openrouter api key for user with id: %s",
            current_user.id
        )
        self._user_service.set_new_openrouter_api_key(
            user=current_user,
            new_openrouter_key=OpenRouterAPIKey(value=data.new_openrouter_api_key),
        )
        logger.info(
            "Changed openrouter api key for user with id: %s",
            current_user.id
        )

        logger.info(
            "Started requesting persistence storage for update user with id: %s",
            current_user.id
        )

        await self._user_command_gateway.update(current_user)

        logger.info("Started commiting transaction")

        await self._transaction_manager.commit()

        logger.info(
            "Finished updating openrouter api key for user with id: %s",
            current_user.id
        )
