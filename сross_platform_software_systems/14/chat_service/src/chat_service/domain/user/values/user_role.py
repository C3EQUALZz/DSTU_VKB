from enum import StrEnum


class UserRole(StrEnum):
    """
    Super admin. For example: Developers, Director, etc.
    Admin. For example: Developers, Director, etc.
    Annotator. User which marks up messages for AI.

    """

    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

    @property
    def is_assignable(self) -> bool:
        return self != UserRole.SUPER_ADMIN

    @property
    def is_changeable(self) -> bool:
        return self != UserRole.SUPER_ADMIN