from dataclasses import dataclass
from uuid import UUID

from cryptography_methods.domain.common.events import BaseDomainEvent


@dataclass(frozen=True)
class UserCreatedEvent(BaseDomainEvent):
    user_id: UUID
    first_name: str
    role: str
    second_name: str | None = None
    middle_name: str | None = None
    telegram_account_id: str | None = None


@dataclass(frozen=True)
class UserChangedFirstNameEvent(BaseDomainEvent):
    user_id: UUID
    first_name: str


@dataclass(frozen=True)
class UserChangedSecondNameEvent(BaseDomainEvent):
    user_id: UUID
    second_name: str


@dataclass(frozen=True)
class UserChangedMiddleNameEvent(BaseDomainEvent):
    user_id: UUID
    middle_name: str


@dataclass(frozen=True)
class UserChangedMiddleNameEvent(BaseDomainEvent):
    user_id: UUID
    middle_name: str


@dataclass(frozen=True)
class UserLinkedTelegramAccountEvent(BaseDomainEvent):
    user_id: UUID
    telegram_account_id: int


@dataclass(frozen=True)
class UserUnLinkedTelegramAccountEvent(BaseDomainEvent):
    user_id: UUID
    telegram_account_id: int


@dataclass(frozen=True)
class UserChangedRoleEvent(BaseDomainEvent):
    user_id: UUID
    role: str


@dataclass(frozen=True)
class UserWasBlockedEvent(BaseDomainEvent):
    user_id: UUID
