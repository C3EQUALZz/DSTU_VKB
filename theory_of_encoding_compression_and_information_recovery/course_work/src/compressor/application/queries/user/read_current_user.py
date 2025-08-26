from dataclasses import dataclass
from typing import Final, final

from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.common.views.users import UserView
from compressor.domain.users.entities.user import User
from compressor.domain.users.values.user_id import UserID


@dataclass(frozen=True, slots=True)
class ReadCurrentTelegramUserQuery:
    ...

@final
class ReadCurrentTelegramUserQueryHandler:
    def __init__(
            self,
            idp: IdentityProvider,
            user_gateway: UserQueryGateway
    ) -> None:
        self._idp: Final[IdentityProvider] = idp
        self._user_gateway: Final[UserQueryGateway] = user_gateway

    async def __call__(self, data: ReadCurrentTelegramUserQuery) -> UserView:
        user_id: UserID = await self._idp.get_current_user_id()
        user: User = await self._user_gateway.read_by_id(user_id)

        return UserView(
            first_name=str(user.username),
            role=str(user.role.value),
            telegram_id=user.telegram.id if user.telegram else None,
            language=user.language.value,
        )
