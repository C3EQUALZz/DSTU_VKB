from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, override

from chat_service.domain.user.entities.user import User
from chat_service.domain.user.services.authorization.base import (
    Permission,
    PermissionContext,
)
from chat_service.domain.user.services.authorization.role_hierarchy import (
    SUBORDINATE_ROLES,
)
from chat_service.domain.user.values.user_role import UserRole


@dataclass(frozen=True, kw_only=True)
class UserManagementContext(PermissionContext):
    subject: User
    target: User


class CanManageSelf(Permission[UserManagementContext]):
    def is_satisfied_by(self, context: UserManagementContext) -> bool:
        return context.subject == context.target


class CanManageSubordinate(Permission[UserManagementContext]):
    def __init__(
        self,
        role_hierarchy: Mapping[UserRole, set[UserRole]] = SUBORDINATE_ROLES,
    ) -> None:
        self._role_hierarchy: Final[Mapping[UserRole, set[UserRole]]] = role_hierarchy

    @override
    def is_satisfied_by(self, context: UserManagementContext) -> bool:
        allowed_roles = self._role_hierarchy.get(context.subject.role, set())
        return context.target.role in allowed_roles


@dataclass(frozen=True, kw_only=True)
class RoleManagementContext(PermissionContext):
    subject: User
    target_role: UserRole


class CanManageRole(Permission[RoleManagementContext]):
    def __init__(
        self,
        role_hierarchy: Mapping[UserRole, set[UserRole]] = SUBORDINATE_ROLES,
    ) -> None:
        self._role_hierarchy: Final[Mapping[UserRole, set[UserRole]]] = role_hierarchy

    @override
    def is_satisfied_by(self, context: RoleManagementContext) -> bool:
        allowed_roles = self._role_hierarchy.get(context.subject.role, set())
        return context.target_role in allowed_roles