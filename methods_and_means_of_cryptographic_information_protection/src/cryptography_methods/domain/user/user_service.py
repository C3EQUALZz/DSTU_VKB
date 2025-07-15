from datetime import datetime, UTC

from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.full_name import FullName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName


class UserService:
    # noinspection PyMethodMayBeStatic
    def change_by_full_name(
            self,
            user: User,
            full_name: FullName
    ) -> None:
        if full_name is None or not isinstance(full_name, FullName):
            raise TypeError(f"Изменение полного имени может быть только с типом FullName, не {type(full_name)}")

        user.change_first_name(FirstName(full_name.first_name))
        user.change_middle_name(MiddleName(full_name.middle_name))
        user.change_second_name(SecondName(full_name.second_name))
        user.updated_at = UpdateTime(datetime.now(UTC))

    # noinspection PyMethodMayBeStatic
    def link_telegram_account(
            self,
            user: User,
            telegram_account: TelegramAccount,
    ) -> None:
        if telegram_account is None or not isinstance(telegram_account, TelegramAccount):
            raise TypeError("Telegram account must be of type TelegramAccount")

        if user is None or not isinstance(user, User):
            raise TypeError("In user you should provide user instance")

