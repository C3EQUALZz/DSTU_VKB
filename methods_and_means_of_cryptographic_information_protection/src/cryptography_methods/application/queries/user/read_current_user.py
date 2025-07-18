from dataclasses import dataclass
from typing import Final, final
from cryptography_methods.application.common.id_provider import IdentityProvider
from cryptography_methods.application.common.ports.user.query_gateway import UserQueryGateway
from cryptography_methods.application.common.views.user import UserView
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.values.user_id import UserID


@dataclass(frozen=True, slots=True)
class ReadCurrentUserQuery:
    ...

@final
class ReadCurrentUserQueryHandler:
    def __init__(
            self,
            idp: IdentityProvider,
            user_gateway: UserQueryGateway
    ) -> None:
        self._idp: Final[IdentityProvider] = idp
        self._user_gateway: Final[UserQueryGateway] = user_gateway

    async def __call__(self, data: ReadCurrentUserQuery) -> UserView:
        user_id: UserID = await self._idp.get_current_user_id()
        user: User = await self._user_gateway.read_by_id(user_id)
        return UserView(
            first_name=str(user.first_name),
            role=str(user.role),
            telegram_id=user.telegram_account.id if user.telegram_account else None,
            last_name=user.second_name if user.second_name else None,
        )