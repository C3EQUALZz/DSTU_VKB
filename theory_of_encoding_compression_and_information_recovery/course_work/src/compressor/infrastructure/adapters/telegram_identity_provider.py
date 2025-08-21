from typing import Final, override

from compressor.domain.users.values.user_role import UserRole
from compressor.application.errors.auth import AuthenticationError
from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.telegram_user_query_gateway import TelegramUserQueryGateway
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID


class TelegramIdentityProvider(IdentityProvider):
    def __init__(
            self,
            telegram_id: TelegramID | None,
            telegram_user_query_gateway: TelegramUserQueryGateway,
    ) -> None:
        self._telegram_id: Final[TelegramID | None] = telegram_id
        self._telegram_user_query_gateway: Final[TelegramUserQueryGateway] = telegram_user_query_gateway

    @override
    async def get_current_user_id(self) -> UserID:
        if not self._telegram_id:
            raise AuthenticationError()

        if current_user := await self._telegram_user_query_gateway.read_by_telegram_id(
                self._telegram_id
        ):
            return current_user.user.id

        raise AuthenticationError()

    @override
    async def get_current_role(self) -> UserRole:
        if not self._telegram_id:
            raise AuthenticationError()

        if (
                current_user := await self._telegram_user_query_gateway.read_by_telegram_id(
                    self._telegram_id
                )
        ):
            return current_user.user.role

        raise AuthenticationError()
