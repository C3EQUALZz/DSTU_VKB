from dataclasses import dataclass, field

from cryptography_methods.domain.common.entities.base_aggregate import BaseAggregateRoot
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.domain.user.values.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class User(BaseAggregateRoot[UserID]):
    first_name: FirstName
    role: UserRole = field(default_factory=lambda: UserRole.USER)
    is_blocked: bool = field(default=False)
    middle_name: MiddleName | None = field(default_factory=lambda: None)
    second_name: SecondName | None = field(default_factory=lambda: None)
    telegram_account: TelegramAccount | None = field(default_factory=lambda: None)
