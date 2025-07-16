from typing import Final

from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import BotCantBeLinkedToUserError, UserAlreadyBlockedError
from cryptography_methods.domain.user.services.access_service import AccessService
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.telegram_id import TelegramID


class TelegramService:
    def __init__(self, authorization_service: AccessService):
        self._authorization_service: Final[AccessService] = authorization_service

    # noinspection PyMethodMayBeStatic
    def create(
            self,
            telegram_id: TelegramID,
            language_code: LanguageCode = LanguageCode.RU,
    ) -> TelegramAccount:
        return TelegramAccount.create(
            telegram_id=telegram_id,
            language_code=language_code,
        )

    def link_telegram_account(
            self,
            user: User,
            telegram_account: TelegramAccount,
    ) -> None:
        if telegram_account is None or not isinstance(telegram_account, TelegramAccount):
            raise TypeError("Telegram account must be of type TelegramAccount")

        if user is None or not isinstance(user, User):
            raise TypeError("In user you should provide user instance")

        if user.is_blocked:
            raise UserAlreadyBlockedError("Cant link telegram account to user which was blocked")

        if telegram_account.is_bot:
            self._authorization_service.block_user(user)
            raise BotCantBeLinkedToUserError("Current telegram id is bot, blocking user for system")

        user.link_telegram_account(telegram_account)

    # noinspection PyMethodMayBeStatic
    def unlink_telegram_account(
            self,
            user: User,
            telegram_account: TelegramAccount,
    ) -> None:
        if telegram_account is None or not isinstance(telegram_account, TelegramAccount):
            raise TypeError(f"Telegram account must be of type TelegramAccount, not {type(telegram_account)}")

        if user is None or not isinstance(user, User):
            raise TypeError(f"In user you should provide User instance, not {type(user)}")

        if user.is_blocked:
            raise UserAlreadyBlockedError("Cant link telegram account to user which was blocked")

        user.unlink_telegram_account(telegram_account)
