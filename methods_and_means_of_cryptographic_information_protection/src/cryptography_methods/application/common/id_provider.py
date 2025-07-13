from abc import abstractmethod
from typing import Protocol

from cryptography_methods.domain.user.values.user_id import UserID


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserID:
        ...
