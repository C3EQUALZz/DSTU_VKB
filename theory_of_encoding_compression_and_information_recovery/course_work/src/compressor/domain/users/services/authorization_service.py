from typing import TypeVar

from compressor.domain.common.services.base import DomainService
from compressor.domain.users.entities.user import User
from compressor.domain.users.errors import (
    ActivationChangeNotPermittedError,
    AuthorizationError,
    RoleChangeNotPermittedError,
)
from compressor.domain.users.services.authorization.base import (
    Permission,
    PermissionContext,
)
from compressor.domain.users.values.user_role import UserRole

PC = TypeVar("PC", bound=PermissionContext)


class AuthorizationService(DomainService):
    def __init__(self) -> None:
        super().__init__()

    # noinspection PyMethodMayBeStatic
    def authorize(self, permission: Permission[PC], *, context: PC) -> None:
        """
        :raises AuthorizationError:
        """
        if not permission.is_satisfied_by(context):
            msg: str = "Not authorized."
            raise AuthorizationError(msg)

    # noinspection PyMethodMayBeStatic
    def toggle_user_activation(self, user: User, *, is_active: bool) -> None:
        """
        :raises ActivationChangeNotPermittedError:
        """
        if not user.role.is_changeable:
            msg: str = f"Changing activation of user {user.username.value!r} ({user.role}) is not permitted."
            raise ActivationChangeNotPermittedError(msg)
        user.is_active = is_active

    # noinspection PyMethodMayBeStatic
    def toggle_user_admin_role(self, user: User, *, is_admin: bool) -> None:
        """
        :raises RoleChangeNotPermittedError:
        """
        if not user.role.is_changeable:
            msg: str = f"Changing role of user {user.username.value!r} ({user.role}) is not permitted."
            raise RoleChangeNotPermittedError(msg)
        user.role = UserRole.ADMIN if is_admin else UserRole.USER
