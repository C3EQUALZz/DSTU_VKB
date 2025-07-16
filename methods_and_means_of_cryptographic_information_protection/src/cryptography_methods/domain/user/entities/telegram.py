from dataclasses import dataclass, field
from typing import Self

from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.telegram_id import TelegramID


@dataclass
class TelegramAccount(BaseEntity[TelegramID]):
    is_bot: bool = False
    language_code: LanguageCode = field(default_factory=lambda: LanguageCode("ru"))

    @classmethod
    def create(
            cls,
            telegram_id: TelegramID,
            language_code: LanguageCode = LanguageCode.RU,
    ) -> Self:
        return cls(
            id=telegram_id,
            language_code=language_code,
        )

    def change_user_bot_status(self, new_status: bool) -> None:
        if new_status is None or not isinstance(new_status, bool):
            raise TypeError(f"New_status must be a boolean value, not {type(new_status)}")
        self.is_bot = new_status

    def change_language_code(self, language_code: LanguageCode) -> None:
        if language_code is None or not isinstance(language_code, LanguageCode):
            raise TypeError(f"Language_code must be of type LanguageCode, not {type(language_code)}")
        self.language_code = language_code
