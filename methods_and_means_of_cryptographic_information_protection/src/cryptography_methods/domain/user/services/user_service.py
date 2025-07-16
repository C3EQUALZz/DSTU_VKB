from typing import Final

from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import RoleAssignmentNotPermittedError
from cryptography_methods.domain.user.ports.user_id_generator import UserIdGenerator
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.full_name import FullName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.domain.user.values.user_role import UserRole


class UserService:
    def __init__(self, user_id_generator: UserIdGenerator) -> None:
        self._user_id_generator: Final[UserIdGenerator] = user_id_generator

    def create(
            self,
            first_name: FirstName,
            role: UserRole,
            second_name: SecondName | None = None,
            middle_name: MiddleName | None = None,
    ) -> User:
        if first_name is None or not isinstance(first_name, FirstName):
            raise TypeError(f"User first name can be of type FirstName, not {type(first_name)}")

        if role is None or not isinstance(role, UserRole):
            raise TypeError(f"User role can be of type UserRole, not {type(role)}")

        if type(second_name) not in (None, SecondName):
            raise TypeError(f"User second name can be of type SecondName or None, not {type(second_name)}")

        if type(middle_name) not in (None, MiddleName):
            raise TypeError(f"User middle_name can be of type MiddleName or None, not {type(middle_name)}")

        if not role.is_assignable:
            raise RoleAssignmentNotPermittedError(f"Assignment of role {role} is not permitted.")

        user_id: UserID = self._user_id_generator()

        new_user: User = User(
            id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            role=role,
            second_name=second_name,
        )

        return new_user

    # noinspection PyMethodMayBeStatic
    def change_by_full_name(
            self,
            user: User,
            full_name: FullName
    ) -> None:
        if user is None or not isinstance(user, User):
            raise TypeError(f"User must be of type User, not {type(user)}")

        if full_name is None or not isinstance(full_name, FullName):
            raise TypeError(f"Изменение полного имени может быть только с типом FullName, не {type(full_name)}")

        user.change_first_name(FirstName(full_name.first_name))
        user.change_middle_name(MiddleName(full_name.middle_name))
        user.change_second_name(SecondName(full_name.second_name))