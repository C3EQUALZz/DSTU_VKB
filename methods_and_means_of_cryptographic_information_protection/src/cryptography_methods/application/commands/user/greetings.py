from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.id_provider import IdentityProvider
from cryptography_methods.application.common.view_manager import ViewManager
from cryptography_methods.domain.user.values.user_id import UserID


@dataclass(frozen=True, slots=True)
class GreetingUserCommand:
    first_name: str


@final
class GreetingUserCommandHandler:
    def __init__(self, view_manager: ViewManager, idp: IdentityProvider) -> None:
        self._view_manager: Final[ViewManager] = view_manager
        self._idp: Final[IdentityProvider] = idp

    async def __call__(self, data: GreetingUserCommand) -> None:
        user_id: UserID = await self._idp.get_current_user_id()
        await self._view_manager.send_greeting_to_user(user_id=user_id)
