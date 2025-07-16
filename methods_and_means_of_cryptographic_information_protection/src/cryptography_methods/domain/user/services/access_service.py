from datetime import datetime, UTC

from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import RoleChangeNotPermittedError, UserAlreadyBlockedError
from cryptography_methods.domain.user.values.user_role import UserRole


class AccessService:
    # noinspection PyMethodMayBeStatic
    def block_user(self, user: User) -> None:
        if user.is_blocked:
            raise UserAlreadyBlockedError(f"Current user: {user.id} is already blocked")
        user.block()

    # noinspection PyMethodMayBeStatic
    def change_role(self, user: User, user_role: UserRole) -> None:
        if user_role is None or not isinstance(user_role, UserRole):
            raise TypeError(f"User role must be of type UserRole, not {type(user_role)}")

        if user is None or not isinstance(user, User):
            raise TypeError(f"User must be of type User, not {type(user)}")

        if not user.role.is_changeable:
            raise RoleChangeNotPermittedError(
                f"Changing role of user {user.first_name} ({user.role.value}) is not permitted."
            )

        if user.is_blocked:
            raise UserAlreadyBlockedError(f"Current user: {user.id} is already blocked")

        user.change_role(user_role)
        user.updated_at = UpdateTime(datetime.now(UTC))
