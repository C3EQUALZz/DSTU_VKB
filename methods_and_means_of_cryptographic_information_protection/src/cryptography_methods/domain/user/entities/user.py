from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Self

from cryptography_methods.domain.common.entities.base_aggregate import BaseAggregateRoot
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_id import UserID


@dataclass
class User(BaseAggregateRoot[UserID]):
    first_name: FirstName
    second_name: SecondName | None = None
    middle_name: MiddleName | None = None
    telegram_account: TelegramAccount | None = None

    @classmethod
    def create(
            cls,
            user_id: UserID,
            first_name: FirstName,
            second_name: SecondName | None = None,
            middle_name: MiddleName | None = None,
            telegram_account: TelegramAccount | None = None
    ) -> Self:
        return cls(
            user_id,
            first_name=first_name,
            second_name=second_name,
            middle_name=middle_name,
            telegram_account=telegram_account,
        )

    def change_first_name(self, first_name: FirstName) -> None:
        if first_name is None or not isinstance(first_name, FirstName):
            raise TypeError(f"Изменение имени может быть только типа FirstName, не {type(first_name)}")
        self.first_name: FirstName = first_name
        self.updated_at = UpdateTime(datetime.now(UTC))

    def change_second_name(self, second_name: SecondName) -> None:
        if second_name is None or not isinstance(second_name, SecondName):
            raise TypeError(f"Изменение фамилии может быть только типа SecondName, не {type(second_name)}")
        self.second_name: SecondName = second_name
        self.updated_at = UpdateTime(datetime.now(UTC))

    def change_middle_name(self, middle_name: MiddleName) -> None:
        if middle_name is None or not isinstance(middle_name, MiddleName):
            raise TypeError(f"Изменение отчества может быть только MiddleName, не {type(middle_name)}")
        self.middle_name: MiddleName = middle_name
        self.updated_at = UpdateTime(datetime.now(UTC))

    def link_telegram_account(self, ):
        ...
