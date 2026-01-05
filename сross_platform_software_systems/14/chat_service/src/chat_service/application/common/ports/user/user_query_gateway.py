from abc import abstractmethod
from typing import Protocol

from chat_service.application.common.query_params.user_filters import UserListParams
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.user_id import UserID


class UserQueryGateway(Protocol):
    @abstractmethod
    async def read_user_by_id(self, user_id: UserID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def read_all_users(self, user_list_params: UserListParams) -> list[User] | None:
        raise NotImplementedError