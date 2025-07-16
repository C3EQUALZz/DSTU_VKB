from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self
from typing_extensions import override
from cryptography_methods.domain.common.entities.base_aggregate import BaseAggregateRoot
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.errors import TelegramAccountHasBeenLinkedError
from cryptography_methods.domain.user.events import (
    UserCreatedEvent,
    UserChangedFirstNameEvent,
    UserChangedSecondNameEvent,
    UserChangedMiddleNameEvent,
    UserLinkedTelegramAccountEvent,
    UserChangedRoleEvent
)
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.domain.user.values.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class User(BaseAggregateRoot[UserID]):
    first_name: FirstName
    role: UserRole
    is_blocked: bool = False
    second_name: SecondName | None = None
    middle_name: MiddleName | None = None
    telegram_account: TelegramAccount | None = None

    @override
    def __post_init__(self) -> None:
        super().__post_init__()

        event: UserCreatedEvent = UserCreatedEvent(
            user_id=self.id,
            first_name=str(self.first_name),
            middle_name=str(self.middle_name) if self.middle_name else None,
            second_name=str(self.second_name) if self.second_name else None,
            telegram_account_id=self.telegram_account.id if self.telegram_account else None,
            role=self.role.value,
        )

        self._register_event(
            event=event,
        )

    @classmethod
    def create(
            cls,
            user_id: UserID,
            first_name: FirstName,
            user_role: UserRole = UserRole.USER,
            second_name: SecondName | None = None,
            middle_name: MiddleName | None = None,
            telegram_account: TelegramAccount | None = None
    ) -> Self:
        new_user: User = cls(
            id=user_id,
            first_name=first_name,
            second_name=second_name,
            middle_name=middle_name,
            telegram_account=telegram_account,
            role=user_role,
        )

        event: UserCreatedEvent = UserCreatedEvent(
            user_id=user_id,
            first_name=str(first_name),
            middle_name=str(middle_name) if middle_name else None,
            second_name=str(second_name) if second_name else None,
            telegram_account_id=new_user.telegram_account.id if new_user.telegram_account else None,
            role=user_role.value,
        )

        cls._register_event(
            new_user,
            event
        )

        return new_user

    def change_first_name(self, first_name: FirstName) -> None:
        if first_name is None or not isinstance(first_name, FirstName):
            raise TypeError(f"Use can use only type FirstName, not {type(first_name)}")

        self.first_name: FirstName = first_name
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedFirstNameEvent = UserChangedFirstNameEvent(
            user_id=self.id,
            first_name=str(first_name),
        )

        self._register_event(event)

    def change_second_name(self, second_name: SecondName) -> None:
        if second_name is None or not isinstance(second_name, SecondName):
            raise TypeError(f"Use can use only type SecondName, not {type(second_name)}")

        self.second_name: SecondName = second_name
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedSecondNameEvent = UserChangedSecondNameEvent(
            user_id=self.id,
            second_name=str(second_name),
        )

        self._register_event(event)

    def change_middle_name(self, middle_name: MiddleName) -> None:
        if middle_name is None or not isinstance(middle_name, MiddleName):
            raise TypeError(f"Изменение отчества может быть только MiddleName, не {type(middle_name)}")

        self.middle_name: MiddleName = middle_name
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedMiddleNameEvent = UserChangedMiddleNameEvent(
            user_id=self.id,
            middle_name=str(middle_name),
        )

        self._register_event(event)

    def link_telegram_account(self, telegram_account: TelegramAccount) -> None:
        if telegram_account is None or not isinstance(telegram_account, TelegramAccount):
            raise TypeError(f"Please provide telegram account type, not {type(telegram_account)}")

        if self.telegram_account is not None:
            raise TelegramAccountHasBeenLinkedError(
                f"Telegram account {telegram_account.id} cant linked to user {self.id}."
                f" User have already linked account before"
            )

        self.telegram_account = telegram_account
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserLinkedTelegramAccountEvent = UserLinkedTelegramAccountEvent(
            user_id=self.id,
            telegram_account_id=self.telegram_account.id,
        )

        self._register_event(event)

    def unlink_telegram_account(self, telegram_account: TelegramAccount) -> None:
        if telegram_account is None or not isinstance(telegram_account, TelegramAccount):
            raise TypeError(f"Please provide telegram account type, not {type(telegram_account)}")

        if self.telegram_account is None:
            ...


    def change_role(self, user_role: UserRole) -> None:
        if user_role is None or not isinstance(user_role, UserRole):
            raise TypeError(f"User role must be of type UserRole, not {type(user_role)}")

        self.role = user_role
        self.updated_at = UpdateTime(datetime.now(UTC))

        self._register_event(
            UserChangedRoleEvent(
                user_id=self.id,
                role=user_role.value,
            )
        )

    def block(self) -> None:
        if self.role == UserRole.SUPER_ADMIN:
            raise ...

        self.is_blocked = True
        self.updated_at = UpdateTime(datetime.now(UTC))
