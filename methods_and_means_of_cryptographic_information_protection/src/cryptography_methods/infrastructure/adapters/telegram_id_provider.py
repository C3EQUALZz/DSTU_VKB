from typing import Iterable, Final

from typing_extensions import override

from cryptography_methods.application.common.id_provider import IdentityProvider
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.infrastructure.errors.id_provider import AuthenticationError


class CompositeIdentityProvider(IdentityProvider):
    def __init__(self, id_providers: Iterable[IdentityProvider]) -> None:
        self.id_providers: Final[Iterable[IdentityProvider]] = id_providers

    @override
    async def get_current_user_id(self) -> UserID:
        for id_provider in self.id_providers:
            user_id: UserID | None = await id_provider.get_current_user_id()
            if user_id:
                return user_id
        raise AuthenticationError("Authentication failed, can't get current user id")


class TelegramIdentityProvider(IdentityProvider):
    def __init__(
            self,
            telegram_id: int | None
    ) -> None:
        self._telegram_id: int | None = telegram_id

    @override
    async def get_current_user_id(self) -> UserID:
        if self._telegram_id is None:
            raise AuthenticationError("Telegram id is not set")
        return UserID(self._telegram_id)
