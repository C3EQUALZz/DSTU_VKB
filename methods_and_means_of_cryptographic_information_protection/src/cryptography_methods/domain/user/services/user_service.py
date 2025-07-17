from typing import Final

from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.ports.user_id_generator import UserIdGenerator
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.full_name import FullName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_role import UserRole


class UserService:
    def __init__(self, user_id_generator: UserIdGenerator) -> None:
        self._user_id_generator: Final[UserIdGenerator] = user_id_generator

    def create(
            self,
            first_name: FirstName,
            middle_name: MiddleName | None = None,
            second_name: SecondName | None = None,
            telegram_account: TelegramAccount | None = None
    ) -> User:
        return User(
            id=self._user_id_generator(),
            first_name=first_name,
            middle_name=middle_name,
            second_name=second_name,
            telegram_account=telegram_account,
            role=UserRole.USER,
        )

    # noinspection PyMethodMayBeStatic
    def update_by_full_name(
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
