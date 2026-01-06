from dataclasses import dataclass

from chat_service.domain.common.events import BaseDomainEvent
from chat_service.domain.user.values.user_id import UserID


@dataclass(frozen=True, slots=True, eq=False)
class UserCreatedEvent(BaseDomainEvent):
    user_id: UserID


@dataclass(frozen=True, slots=True, eq=False)
class UserChangedUserNameEvent(BaseDomainEvent):
    user_id: UserID

@dataclass(frozen=True, slots=True, eq=False)
class UserChangedRoleEvent(BaseDomainEvent):
    user_id: UserID
    old_role: str
    new_role: str


@dataclass(frozen=True, slots=True, eq=False)
class UserToggleActivationEvent(BaseDomainEvent):
    user_id: UserID
    is_active: bool