import logging
from datetime import datetime, UTC
from typing import overload, Final

from chat_service.domain.common.services.base import DomainService
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.events import UserCreatedEvent, UserChangedUserNameEvent
from chat_service.domain.user.values.open_router_api_key import OpenRouterAPIKey
from chat_service.domain.user.values.user_id import UserID
from chat_service.domain.user.values.user_name import UserName

logger: Final[logging.Logger] = logging.getLogger(__name__)


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

    def create(
            self,
            user_id: UserID,
            name: UserName,
            openrouter_api_key: OpenRouterAPIKey | None = None,
    ) -> User:
        logger.debug(
            "Started creating new user with user id: %s, name: %s, openrouter_api_key: %s",
            user_id,
            name,
            openrouter_api_key
        )

        new_entity: User = User(
            id=user_id,
            name=name,
            openrouter_api_key=openrouter_api_key,
        )

        logger.debug("New entity: %s", new_entity)

        new_event: UserCreatedEvent = UserCreatedEvent(
            user_id=user_id,
        )

        self._record_event(new_event)

        logger.debug(
            "User new event: %s",
            new_event
        )

        return new_entity

    def change_user_name(
            self,
            user: User,
            new_name: UserName
    ) -> None:
        logger.debug(
            "Started changing user %s name with new name: %s",
            user.id,
            new_name
        )

        user.name = new_name
        user.updated_at = datetime.now(UTC)

        new_event: UserChangedUserNameEvent = UserChangedUserNameEvent(
            user_id=user.id,
        )

        self._record_event(new_event)

        logger.debug("User new event: %s", new_event)

    # noinspection PyMethodMayBeStatic
    def set_new_openrouter_api_key(
            self,
            user: User,
            new_openrouter_key: OpenRouterAPIKey
    ) -> None:
        logger.debug(
            "User started setting new openrouter_api_key: %s",
            new_openrouter_key
        )

        user.openrouter_api_key = new_openrouter_key
        user.updated_at = datetime.now(UTC)
