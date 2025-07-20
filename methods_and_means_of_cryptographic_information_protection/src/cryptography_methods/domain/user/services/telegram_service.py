from datetime import datetime, UTC
from typing import Final

from cryptography_methods.domain.common.services import DomainService
from cryptography_methods.domain.common.values import UpdateTime
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.errors import (
    BotCantBeLinkedToUserError,
    UserAlreadyBlockedError,
    TelegramAccountHasBeenLinkedError,
    CantUnLinkUnexistingAccountError
)
from cryptography_methods.domain.user.events import (
    UserLinkedTelegramAccountEvent,
    UserUnLinkedTelegramAccountEvent,
    UserWasBlockedEvent
)
from cryptography_methods.domain.user.services.access_service import AccessService
from cryptography_methods.domain.user.values.language_code import LanguageCode
from cryptography_methods.domain.user.values.telegram_id import TelegramID


class TelegramService(DomainService):
    def __init__(self, access_service: AccessService) -> None:
        super().__init__()
        self._access_service: Final[AccessService] = access_service

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

    def mark_telegram_account_as_bot(
            self,
            user: User,
            telegram_account: TelegramAccount
    ) -> None:
        if not isinstance(telegram_account, TelegramAccount):
            raise TypeError("Invalid telegram account type")

        if not isinstance(user, User):
            raise TypeError("Invalid user type")

        if telegram_account.is_bot:
            return

        # Обновление статуса аккаунта
        telegram_account.is_bot = True

        # Блокировка пользователя
        self._access_service.block_user(user)

        # Генерация события
        self._record_event(UserWasBlockedEvent(
            user_id=user.id,
        ))

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

        if user.telegram_account is not None:
            raise TelegramAccountHasBeenLinkedError(
                f"Telegram account {telegram_account.id} cant linked to user {user.id}."
                f" User have already linked account before"
            )

        user.telegram_account = telegram_account
        user.updated_at = UpdateTime(datetime.now(UTC))

        event: UserLinkedTelegramAccountEvent = UserLinkedTelegramAccountEvent(
            user_id=user.id,
            telegram_account_id=user.telegram_account.id,
        )

        self._record_event(event)

    def unlink_telegram_account(
            self,
            user: User
    ) -> None:
        if user is None or not isinstance(user, User):
            raise TypeError(f"In user you should provide User instance, not {type(user)}")

        if user.telegram_account is None:
            raise CantUnLinkUnexistingAccountError(
                f"Telegram account cant unlink, id: {user.id} doesnt have telegram account"
            )

        if user.is_blocked:
            raise UserAlreadyBlockedError("Cant link telegram account to user which was blocked")

        telegram_id: TelegramID = user.telegram_account.id
        user.telegram_account = None

        event: UserUnLinkedTelegramAccountEvent = UserUnLinkedTelegramAccountEvent(
            user_id=user.id,
            telegram_account_id=telegram_id,
        )

        self._record_event(event)

    # noinspection PyMethodMayBeStatic
    def change_language_code(self, user: User, language_code: LanguageCode) -> None:
        if user is None or not isinstance(user, User):
            raise TypeError(f"In user you should provide User instance, not {type(user)}")

        user.language_code = language_code
        user.updated_at = UpdateTime(datetime.now(UTC))

