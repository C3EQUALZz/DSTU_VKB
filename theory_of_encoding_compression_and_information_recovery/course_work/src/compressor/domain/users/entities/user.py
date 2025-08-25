from dataclasses import dataclass, field

from compressor.domain.common.entities.base_aggregate import BaseAggregateRoot
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.values.language_code import LanguageCode
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_password_hash import UserPasswordHash
from compressor.domain.users.values.user_role import UserRole
from compressor.domain.users.values.username import Username


@dataclass(eq=False, kw_only=True)
class User(BaseAggregateRoot[UserID]):
    username: Username
    password_hash: UserPasswordHash
    role: UserRole
    is_active: bool
    telegram: TelegramUser | None = field(default=None)
    language: LanguageCode = field(default_factory=lambda: LanguageCode("ru"))
