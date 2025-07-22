from datetime import datetime, UTC
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.events import (
    UserCreatedEvent,
    UserChangedFirstNameEvent,
    UserChangedSecondNameEvent,
    UserChangedMiddleNameEvent,
    UserChangedFullNameEvent
)
from cryptography_methods.domain.user.ports.user_id_generator import UserIdGenerator
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.full_name import FullName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_role import UserRole


class UserService(DomainService):
    def __init__(self, user_id_generator: UserIdGenerator) -> None:
        super().__init__()
        self._user_id_generator: Final[UserIdGenerator] = user_id_generator

    def create(
            self,
            first_name: FirstName,
            middle_name: MiddleName | None = None,
            second_name: SecondName | None = None,
            telegram_account: TelegramAccount | None = None
    ) -> User:
        new_user = User(
            id=self._user_id_generator(),
            first_name=first_name,
            middle_name=middle_name,
            second_name=second_name,
            telegram_account=telegram_account,
            role=UserRole.USER,
        )

        event: UserCreatedEvent = UserCreatedEvent(
            user_id=new_user.id,
            first_name=str(new_user.first_name),
            middle_name=str(new_user.middle_name) if new_user.middle_name else None,
            second_name=str(new_user.second_name) if new_user.second_name else None,
            telegram_account_id=new_user.telegram_account.id if new_user.telegram_account else None,
            role=new_user.role.value,
        )

        self._record_event(
            event=event,
        )

        return new_user

    def change_first_name(self, user: User, new_first_name: FirstName) -> None:
        if new_first_name is None or not isinstance(new_first_name, FirstName):
            raise TypeError("First name must be of type FirstName")

        if user is not None or not isinstance(user, User):
            raise TypeError("User must be of type User")

        if user.first_name == new_first_name:
            return

        user.first_name = new_first_name
        user.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedFirstNameEvent = UserChangedFirstNameEvent(
            user_id=user.id,
            first_name=str(user.first_name),
        )

        self._record_event(event)

    def change_second_name(self, user: User, new_second_name: SecondName) -> None:
        if new_second_name is None or not isinstance(new_second_name, SecondName):
            raise TypeError("Second name must be of type SecondName")
        if user is not None or not isinstance(user, User):
            raise TypeError("User must be of type User")

        if user.second_name == new_second_name:
            return

        user.second_name = new_second_name
        user.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedSecondNameEvent = UserChangedSecondNameEvent(
            user_id=user.id,
            second_name=str(user.second_name),
        )

        self._record_event(event)

    def change_middle_name(self, user: User, new_middle_name: MiddleName) -> None:
        if new_middle_name is None or not isinstance(new_middle_name, MiddleName):
            raise TypeError(f"Use can use only type MiddleName, not {type(new_middle_name)}")

        user.middle_name = new_middle_name
        user.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedMiddleNameEvent = UserChangedMiddleNameEvent(
            user_id=user.id,
            middle_name=str(user.middle_name),
        )

        self._record_event(event)

    def change_by_full_name(
            self,
            user: User,
            full_name: FullName
    ) -> None:
        if user is None or not isinstance(user, User):
            raise TypeError(f"User must be of type User, not {type(user)}")

        if full_name is None or not isinstance(full_name, FullName):
            raise TypeError(f"Изменение полного имени может быть только с типом FullName, не {type(full_name)}")

        user.first_name = FirstName(full_name.first_name)
        user.middle_name = MiddleName(full_name.middle_name)
        user.second_name = SecondName(full_name.second_name)
        user.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedFullNameEvent = UserChangedFullNameEvent(
            user_id=user.id,
            first_name=str(user.first_name),
            middle_name=str(user.middle_name),
            second_name=str(user.second_name),
        )

        self._record_event(
            event=event,
        )
