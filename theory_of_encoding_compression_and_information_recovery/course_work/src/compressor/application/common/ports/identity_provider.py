from abc import abstractmethod
from typing import Protocol

from typing_extensions import override

from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_role import UserRole


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserID | None:
        ...

    @abstractmethod
    async def get_current_role(self) -> UserRole | None:
        ...


class CompositeIdentityProvider(IdentityProvider):
    def __init__(self, *id_providers: IdentityProvider) -> None:
        self._id_providers: tuple[IdentityProvider, ...] = id_providers

    @override
    async def get_current_user_id(self) -> UserID | None:
        for id_provider in self._id_providers:
            user_id: UserID = await id_provider.get_current_user_id()
            if user_id:
                return user_id
        return None

    @override
    async def get_current_role(self) -> UserRole | None:
        for id_provider in self._id_providers:
            user_role: UserRole = await id_provider.get_current_role()
            if user_role:
                return user_role
        return None
