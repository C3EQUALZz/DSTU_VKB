from dataclasses import dataclass
from typing import Final, final

from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.user.telegram_user_query_gateway import TelegramUserQueryGateway
from compressor.application.common.views.users import TelegramUserView
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.values.user_id import UserID


@dataclass(frozen=True, slots=True)
class ReadCurrentTelegramUserQuery:
    ...

@final
class ReadCurrentTelegramUserQueryHandler:
    def __init__(
            self,
            idp: IdentityProvider,
            user_gateway: TelegramUserQueryGateway
    ) -> None:
        self._idp: Final[IdentityProvider] = idp
        self._user_gateway: Final[TelegramUserQueryGateway] = user_gateway

    async def __call__(self, data: ReadCurrentTelegramUserQuery) -> TelegramUserView:
        user_id: UserID = await self._idp.get_current_user_id()
        telegram_user: TelegramUser = await self._user_gateway.read_by_id(user_id)

        return TelegramUserView(
            first_name=str(telegram_user.telegram_username),
            role=str(telegram_user.user.role),
            telegram_id=telegram_user.id,
            language=telegram_user.language.value
        )