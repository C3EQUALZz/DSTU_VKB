from abc import abstractmethod
from typing import Protocol

from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserID:
        raise NotImplementedError

    @abstractmethod
    async def get_current_role(self) -> UserRole:
        raise NotImplementedError
