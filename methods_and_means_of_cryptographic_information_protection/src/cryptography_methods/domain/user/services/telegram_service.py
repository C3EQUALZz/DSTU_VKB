from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import BotCantBeLinkedToUserError, UserAlreadyBlockedError
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.telegram_id import TelegramID


class TelegramService:
    # noinspection PyMethodMayBeStatic
    def create(
            self,
            id: TelegramID,
            is_bot: bool = False,
            language_code: LanguageCode = LanguageCode("ru")
    ) -> TelegramAccount:
        return TelegramAccount(
            id=id,
            is_bot=is_bot,
            language_code=language_code,
        )

    # noinspection PyMethodMayBeStatic
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
            raise BotCantBeLinkedToUserError("Current telegram id is bot, blocking user for system")

        user.telegram_account = telegram_account

    # noinspection PyMethodMayBeStatic
    def unlink_telegram_account(
            self,
            user: User
    ) -> None:
        if user is None or not isinstance(user, User):
            raise TypeError(f"In user you should provide User instance, not {type(user)}")

        if user.is_blocked:
            raise UserAlreadyBlockedError("Cant link telegram account to user which was blocked")

        user.telegram_account = None
