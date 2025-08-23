from typing import Final

from typing_extensions import override

from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.user.telegram_user_query_gateway import TelegramUserQueryGateway
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole


class TelegramIdentityProvider(IdentityProvider):
    def __init__(
            self,
            telegram_id: TelegramID | None,
            telegram_user_query_gateway: TelegramUserQueryGateway,
    ) -> None:
        self._telegram_id: Final[TelegramID | None] = telegram_id
        self._telegram_user_query_gateway: Final[TelegramUserQueryGateway] = telegram_user_query_gateway

    @override
    async def get_current_user_id(self) -> UserID | None:
        if not self._telegram_id:
            return None

        if current_user := await self._telegram_user_query_gateway.read_by_telegram_id(
                self._telegram_id
        ):
            return current_user.user.id

        return None

    @override
    async def get_current_role(self) -> UserRole | None:
        if not self._telegram_id:
            return None

        if (
                current_user := await self._telegram_user_query_gateway.read_by_telegram_id(
                    self._telegram_id
                )
        ):
            return current_user.user.role

        return None
