from dataclasses import dataclass, field
from typing import Self

from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.telegram_id import TelegramID
from cryptography_methods.domain.user.values.user_name import UserName


@dataclass
class TelegramAccount(BaseEntity[TelegramID]):
    first_name: FirstName
    is_bot: bool = False
    middle_name: MiddleName | None = None
    user_name: UserName | None = None
    language_code: LanguageCode = field(default_factory=lambda: LanguageCode("ru"))

    @classmethod
    def create(
            cls,
            telegram_id: TelegramID,
            first_name: FirstName,
            middle_name: MiddleName | None = None,
            user_name: UserName | None = None,
            language_code: LanguageCode = LanguageCode.RU,
    ) -> Self:
        return cls(
            id=telegram_id,
            first_name=first_name,
            middle_name=middle_name,
            language_code=language_code,
            user_name=user_name,
        )

    def change_user_bot_status(self, new_status: bool) -> None:
        if new_status is None or not isinstance(new_status, bool):
            raise TypeError("new_status must be a boolean value")
        self.is_bot = new_status

    def change_language_code(self, language_code: LanguageCode) -> None:
        if language_code is None or not isinstance(language_code, LanguageCode):
            raise TypeError("language_code must be of type LanguageCode")
        self.language_code = language_code

