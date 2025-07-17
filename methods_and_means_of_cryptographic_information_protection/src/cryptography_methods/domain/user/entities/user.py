from dataclasses import dataclass
from datetime import datetime, UTC

from cryptography_methods.domain.common.entities.base_aggregate import BaseAggregateRoot
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.errors import (
    TelegramAccountHasBeenLinkedError,
    CantUnLinkUnexistingAccountError,
    RoleChangeNotPermittedError,
    UserAlreadyBlockedError,
    CantBlockSuperUserError
)
from cryptography_methods.domain.user.events import (
    UserCreatedEvent,
    UserChangedFirstNameEvent,
    UserChangedSecondNameEvent,
    UserChangedMiddleNameEvent,
    UserLinkedTelegramAccountEvent,
    UserChangedRoleEvent,
    UserUnLinkedTelegramAccountEvent,
    UserWasBlockedEvent
)
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.domain.user.values.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class User(BaseAggregateRoot[UserID]):
    def __init__(
            self,
            id: UserID,
            *,
            first_name: FirstName,
            role: UserRole,
            middle_name: MiddleName | None = None,
            second_name: SecondName | None = None,
            telegram_account: TelegramAccount | None = None
    ) -> None:
        super().__init__(id)
        self.first_name: FirstName = first_name
        self.second_name: SecondName = second_name
        self.role: UserRole = role
        self.middle_name: MiddleName | None = middle_name
        self.telegram_account: TelegramAccount | None = telegram_account

        event: UserCreatedEvent = UserCreatedEvent(
            user_id=id,
            first_name=str(first_name),
            middle_name=str(middle_name) if middle_name else None,
            second_name=str(second_name) if second_name else None,
            telegram_account_id=self.telegram_account.id if self.telegram_account else None,
            role=self.role.value,
        )

        self._register_event(
            event=event,
        )

    @property
    def first_name(self) -> FirstName:
        return self._first_name

    @first_name.setter
    def first_name(self, value: FirstName) -> None:
        if value is None or not isinstance(value, FirstName):
            raise TypeError("First name must be of type FirstName")

        self._first_name: FirstName = value
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedFirstNameEvent = UserChangedFirstNameEvent(
            user_id=self.id,
            first_name=str(value),
        )

        self._register_event(event)

    @property
    def second_name(self) -> SecondName | None:
        return self._second_name

    @second_name.setter
    def second_name(self, value: SecondName) -> None:
        if value is None or not isinstance(value, SecondName):
            raise TypeError(f"Use can use only type SecondName, not {type(value)}")

        self._second_name: SecondName = value
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedSecondNameEvent = UserChangedSecondNameEvent(
            user_id=self.id,
            second_name=str(value),
        )

        self._register_event(event)

    @property
    def middle_name(self) -> MiddleName | None:
        return self._middle_name

    @middle_name.setter
    def middle_name(self, value: MiddleName) -> None:
        if value is None or not isinstance(value, MiddleName):
            raise TypeError(f"Use can use only type MiddleName, not {type(value)}")

        self._middle_name: MiddleName = value
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserChangedMiddleNameEvent = UserChangedMiddleNameEvent(
            user_id=self.id,
            middle_name=str(value),
        )

        self._register_event(event)

    @property
    def telegram_account(self) -> TelegramAccount | None:
        return self._telegram_account

    @telegram_account.setter
    def telegram_account(self, value: TelegramAccount) -> None:
        if type(value) not in (TelegramAccount, None):
            raise TypeError("TelegramAccount must be of type TelegramAccount or None")

        if type(value) is TelegramAccount:
            self._link_telegram_account(value)

        if value is None:
            self._unlink_telegram_account()

    def _link_telegram_account(self, telegram_account: TelegramAccount) -> None:
        if telegram_account is None or not isinstance(telegram_account, TelegramAccount):
            raise TypeError(f"Please provide telegram account type, not {type(telegram_account)}")

        if self.telegram_account is not None:
            raise TelegramAccountHasBeenLinkedError(
                f"Telegram account {telegram_account.id} cant linked to user {self.id}."
                f" User have already linked account before"
            )

        self._telegram_account: TelegramAccount = telegram_account
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserLinkedTelegramAccountEvent = UserLinkedTelegramAccountEvent(
            user_id=self.id,
            telegram_account_id=self.telegram_account.id,
        )

        self._register_event(event)

    def _unlink_telegram_account(self) -> None:
        if self.telegram_account is None:
            raise CantUnLinkUnexistingAccountError(
                f"Telegram account cant unlink, id: {self.id} doesnt have telegram account"
            )

        telegram_id = self.telegram_account.id
        self._telegram_account: None = None

        event: UserUnLinkedTelegramAccountEvent = UserUnLinkedTelegramAccountEvent(
            user_id=self.id,
            telegram_account_id=telegram_id,
        )

        self._register_event(event)

    @property
    def role(self) -> UserRole:
        return self._role

    @role.setter
    def role(self, value: UserRole) -> None:
        if value is None or not isinstance(value, UserRole):
            raise TypeError("User role must be of type UserRole")

        if not self.role.is_changeable:
            raise RoleChangeNotPermittedError(
                f"Changing role of user {self.first_name} ({self.role.value}) is not permitted."
            )

        if self.is_blocked:
            raise UserAlreadyBlockedError(f"Current user: {self.id} is already blocked")

        if self.role == value:
            return

        self._role: UserRole = value
        self.updated_at = UpdateTime(datetime.now(UTC))

        self._register_event(
            UserChangedRoleEvent(
                user_id=self.id,
                role=self.role.value,
            )
        )

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    @is_blocked.setter
    def is_blocked(self, value: bool) -> None:
        if value is True and self.role == UserRole.SUPER_ADMIN:
            raise CantBlockSuperUserError(f"{self.id} cant be blocked, because it is super admin")

        self._is_blocked: bool = value
        self.updated_at = UpdateTime(datetime.now(UTC))

        event: UserWasBlockedEvent = UserWasBlockedEvent(
            user_id=self.id,
        )

        self._register_event(event)
