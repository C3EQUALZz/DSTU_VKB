from dataclasses import dataclass, field

from chat_service.domain.common.entities.base_entity import BaseEntity
from chat_service.domain.user.values.user_id import UserID
from chat_service.domain.user.values.user_name import UserName
from chat_service.domain.user.values.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class User(BaseEntity[UserID]):
    """User entity in chat service context.

    This is a minimal representation of a user, containing only
    the information needed for the chat service to function.
    The full user data is managed in the user_service.
    """

    name: UserName
    role: UserRole = field(default_factory=lambda: UserRole.USER)
    is_active: bool = field(default_factory=lambda: True)