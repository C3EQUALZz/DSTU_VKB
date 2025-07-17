from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import RoleChangeNotPermittedError, UserAlreadyBlockedError, AccessError
from cryptography_methods.domain.user.values.user_role import UserRole


class AccessService:
    # noinspection PyMethodMayBeStatic
    def block_user(self, user: User) -> None:
        if user.is_blocked:
            raise UserAlreadyBlockedError(f"Current user: {user.id} is already blocked")
        user.is_blocked = True

    # noinspection PyMethodMayBeStatic
    def ensure_is_active(self, user: User) -> bool:
        return not user.is_blocked

    # noinspection PyMethodMayBeStatic
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

        if recipient.role.is_changeable and recipient.role.is_changeable:
            recipient.role = role
