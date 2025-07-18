from dataclasses import dataclass, field

from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.telegram_id import TelegramID


@dataclass(eq=False, kw_only=True)
class TelegramAccount(BaseEntity[TelegramID]):
    is_bot: bool = False,
    language_code: LanguageCode = field(default_factory=lambda: LanguageCode("ru"))