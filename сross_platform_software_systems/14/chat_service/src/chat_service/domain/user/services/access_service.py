from chat_service.domain.common.services.base import DomainService
from chat_service.domain.user.entities.user import User
from chat_service.domain.user.errors import (
    ActivationChangeNotPermittedError,
    AuthorizationError,
    RoleChangeNotPermittedError,
)
from chat_service.domain.user.events import UserChangedRoleEvent, UserToggleActivationEvent
from chat_service.domain.user.services.authorization.base import (
    Permission,
    PermissionContext,
)
from chat_service.domain.user.services.authorization.constants import AUTHZ_NOT_AUTHORIZED
from chat_service.domain.user.values.user_role import UserRole


class AccessService(DomainService):
    def __init__(self) -> None:
        super().__init__()

    def toggle_user_admin_role(self, user: User, *, is_admin: bool) -> None:
        """
        :raises RoleChangeNotPermitted:
        """
        if not user.role.is_changeable:
            msg: str = f"Changing role of user {user.name.value!r} ({user.role}) is not permitted."
            raise RoleChangeNotPermittedError(msg)

        old_role: str = user.role

        user.role = UserRole.ADMIN if is_admin else UserRole.USER

        new_event: UserChangedRoleEvent = UserChangedRoleEvent(
            user_id=user.id,
            old_role=old_role,
            new_role=user.role,
        )

        self._record_event(new_event)

    def toggle_user_activation(self, user: User, *, is_active: bool) -> None:
        """
        :raises ActivationChangeNotPermitted:
        """
        if not user.role.is_changeable:
            msg: str = f"Changing activation of user {user.name.value!r} ({user.role}) is not permitted."
            raise ActivationChangeNotPermittedError(msg)

        user.is_active = is_active

        new_event: UserToggleActivationEvent = UserToggleActivationEvent(
            user_id=user.id,
            is_active=is_active,
        )

        self._record_event(new_event)

    # noinspection PyMethodMayBeStatic
    def authorize[PC: PermissionContext](
        self,
        permission: Permission[PC],
        *,
        context: PC,
    ) -> None:
        """
        :raises AuthorizationError:
        """
        if not permission.is_satisfied_by(context):
            raise AuthorizationError(AUTHZ_NOT_AUTHORIZED)