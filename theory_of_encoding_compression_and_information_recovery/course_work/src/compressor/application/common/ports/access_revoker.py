from abc import abstractmethod
from typing import Protocol

from compressor.domain.users.values.user_id import UserID


class AccessRevoker(Protocol):
    @abstractmethod
    async def remove_all_user_access(self, user_id: UserID) -> None:
        """
        :raises DataMapperError:
        """
        ...
