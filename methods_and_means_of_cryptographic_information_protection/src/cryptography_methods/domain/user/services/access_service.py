from datetime import datetime, UTC

from cryptography_methods.domain.common.services import DomainService
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import (
    RoleChangeNotPermittedError,
    UserAlreadyBlockedError,
    AccessError,
    CantBlockSuperUserError
)
from cryptography_methods.domain.user.events import UserWasBlockedEvent, UserChangedRoleEvent
from cryptography_methods.domain.user.values.user_role import UserRole


class AccessService(DomainService):
    def block_user(self, user: User) -> None:
        if user.role == UserRole.SUPER_ADMIN:
            raise CantBlockSuperUserError(f"{user.id} cant be blocked, because it is super admin")

        if user.is_blocked:
            raise UserAlreadyBlockedError(f"Current user: {user.id} is already blocked")

        user.is_blocked = True
        user.updated_at = UpdateTime(datetime.now(UTC))

        event: UserWasBlockedEvent = UserWasBlockedEvent(
            user_id=user.id,
        )

        self._record_event(event)

    def grant_role_to_user(
            self,
            grantor: User,
            recipient: User,
            role: UserRole
    ) -> None:
        if grantor.is_blocked or recipient.is_blocked:
            raise RoleChangeNotPermittedError("User is already blocked")

        if grantor.role == recipient.role:
            raise AccessError("Grantor has same role as recipient")

        if grantor.role not in (UserRole.ADMIN, UserRole.SUPER_ADMIN):
            raise AccessError("Grantor must have admin or super admin role")

        if not recipient.role.is_changeable or not recipient.role.is_changeable:
            raise AccessError("Grantor must have admin or super admin role")

        recipient.role = role

        event: UserChangedRoleEvent = UserChangedRoleEvent(
            user_id=recipient.id,
            role=recipient.role.value,
        )

        self._record_event(event)
