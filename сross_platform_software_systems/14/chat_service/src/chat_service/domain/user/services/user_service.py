from datetime import datetime, UTC
from typing import overload

from chat_service.domain.common.services.base import DomainService
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.values.open_router_api_key import OpenRouterAPIKey
from chat_service.domain.user.values.user_id import UserID
from chat_service.domain.user.values.user_name import UserName


class UserService(DomainService):
    def __init__(self) -> None:
        super().__init__()

    @overload
    def create(
            self,
            user_id: UserID,
            name: UserName,
    ) -> User:
        ...

    @overload
    def create(
            self,
            user_id: UserID,
            name: UserName,
            openrouter_api_key: OpenRouterAPIKey,
    ) -> User:
        ...

    # noinspection PyMethodMayBeStatic
    def create(
            self,
            user_id: UserID,
            name: UserName,
            openrouter_api_key: OpenRouterAPIKey | None = None,
    ) -> User:
        return User(
            id=user_id,
            name=name,
            openrouter_api_key=openrouter_api_key,
        )

    # noinspection PyMethodMayBeStatic
    def change_user_name(
            self,
            user: User,
            new_name: UserName
    ) -> None:
        user.name = new_name
        user.updated_at = datetime.now(UTC)

    # noinspection PyMethodMayBeStatic
    def set_new_openrouter_api_key(
            self,
            user: User,
            new_openrouter_key: OpenRouterAPIKey
    ) -> None:
        user.openrouter_api_key = new_openrouter_key
        user.updated_at = datetime.now(UTC)
