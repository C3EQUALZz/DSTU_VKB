from datetime import datetime

from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.telegram_id import TelegramID


class TelegramAccount(BaseEntity[TelegramID]):
    def __init__(
            self,
            id: TelegramID,
            is_bot: bool = False,
            language_code: LanguageCode = LanguageCode("ru")
    ) -> None:
        super().__init__(id)
        self.is_bot: bool = is_bot
        self.language_code: LanguageCode = language_code

    @property
    def is_bot(self) -> bool:
        return self._is_bot

    @is_bot.setter
    def is_bot(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("is_bot must be a boolean value, not {type(new_status)}")
        self._is_bot: bool = value
        self.updated_at = UpdateTime(datetime.now())

    @property
    def language_code(self) -> LanguageCode:
        return self._language_code

    @language_code.setter
    def language_code(self, value: LanguageCode) -> None:
        if value is None or not isinstance(value, LanguageCode):
            raise TypeError(f"Language_code must be of type LanguageCode, not {type(value)}")
        self._language_code: LanguageCode = value
        self.updated_at = UpdateTime(datetime.now())
