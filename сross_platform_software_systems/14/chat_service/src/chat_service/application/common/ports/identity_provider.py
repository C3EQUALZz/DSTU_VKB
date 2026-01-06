from abc import abstractmethod
from typing import Protocol

from chat_service.domain.user.values.user_id import UserID


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserID:
        """
        Interface for getting user info.
        For more information, see: https://t.me/advice17_chat/4929
        :raises AuthenticationError:
        """
        ...
