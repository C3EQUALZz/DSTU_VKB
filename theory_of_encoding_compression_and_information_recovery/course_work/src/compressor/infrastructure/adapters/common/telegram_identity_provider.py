import logging
from typing import TYPE_CHECKING, Final

from typing_extensions import override

from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole

if TYPE_CHECKING:
    from compressor.domain.users.entities.user import User

logger: Final[logging.Logger] = logging.getLogger(__name__)


class TelegramIdentityProvider(IdentityProvider):
    def __init__(
        self,
        telegram_id: TelegramID | None,
        telegram_user_query_gateway: UserQueryGateway,
    ) -> None:
        self._telegram_id: Final[TelegramID | None] = telegram_id
        self._telegram_user_query_gateway: Final[UserQueryGateway] = telegram_user_query_gateway

    @override
    async def get_current_user_id(self) -> UserID | None:
        logger.debug("Started getting current user id: %s", self._telegram_id)

        if not self._telegram_id:
            logger.debug("Current telegram id is None, returning None")
            return None

        current_user: User | None = await self._telegram_user_query_gateway.read_by_telegram_id(self._telegram_id)

        if current_user is not None:
            logger.debug("Got current user, user id: %s", current_user.id)
            return current_user.id

        return None

    @override
    async def get_current_role(self) -> UserRole | None:
        logger.debug("Started getting current user role: %s", self._telegram_id)

        if not self._telegram_id:
            logger.debug("Current telegram id is None, returning None")
            return None

        current_user: User | None = await self._telegram_user_query_gateway.read_by_telegram_id(self._telegram_id)

        if current_user is not None:
            logger.debug("Got current user, user id: %s, role: %s", current_user.id, current_user.role)
            return current_user.role

        return None
