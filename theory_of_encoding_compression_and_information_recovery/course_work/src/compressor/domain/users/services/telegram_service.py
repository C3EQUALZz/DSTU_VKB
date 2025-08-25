from typing import Final

from compressor.domain.common.services.base import DomainService
from compressor.domain.users.constants import (
    MIN_TELEGRAM_ID_VALUE,
    MIN_TELEGRAM_USERNAME_LENGTH,
    MAX_TELEGRAM_USERNAME_LENGTH
)
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.errors import TelegramIDMustBePositiveError, InvalidTelegramUsernameError
from compressor.domain.users.events import TelegramUserCreatedEvent, TelegramUserUpdatedEvent
from compressor.domain.users.services.user_service import UserService
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_first_name import UserFirstName
from compressor.domain.users.values.username import Username


class TelegramService(DomainService):
    def __init__(self, user_service: UserService) -> None:
        super().__init__()
        self._user_service: Final[UserService] = user_service

    def create(
            self,
            telegram_id: TelegramID,
            first_name: UserFirstName,
            username: Username | None = None,
            last_name: str | None = None,
            is_premium: bool = False,
            is_bot: bool = False
    ) -> TelegramUser:
        if telegram_id < MIN_TELEGRAM_ID_VALUE:
            msg: str = "Telegram ID must be positive number, please check your input"
            raise TelegramIDMustBePositiveError(msg)

        username_length: int = len(username)
        if not (
                MIN_TELEGRAM_USERNAME_LENGTH
                <= username_length
                <= MAX_TELEGRAM_USERNAME_LENGTH
        ):
            msg: str = (
                f"Length of telegram username must be between"
                f" {MIN_TELEGRAM_USERNAME_LENGTH} and {MAX_TELEGRAM_USERNAME_LENGTH}"
            )
            raise InvalidTelegramUsernameError(msg)

        self._record_event(
            TelegramUserCreatedEvent(
                telegram_id=telegram_id,
                first_name=first_name.value,
                username=username.value,
                is_premium=is_premium,
                is_bot=is_bot,
                last_name=last_name
            )
        )

        return TelegramUser(
            id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            is_premium=is_premium,
            is_bot=is_bot,
        )

    def change_username(self, telegram_user: TelegramUser, new_username: Username) -> None:
        username_length: int = len(new_username)
        if not (
                MIN_TELEGRAM_USERNAME_LENGTH
                <= username_length
                <= MAX_TELEGRAM_USERNAME_LENGTH
        ):
            msg: str = (
                f"Length of telegram username must be between"
                f" {MIN_TELEGRAM_USERNAME_LENGTH} and {MAX_TELEGRAM_USERNAME_LENGTH}"
            )
            raise InvalidTelegramUsernameError(msg)

        telegram_user.telegram_username = new_username

        self._record_event(
            TelegramUserUpdatedEvent(
                telegram_id=telegram_user.id,
                username=new_username.value,
            )
        )

    def change_first_name(self, telegram_user: TelegramUser, new_first_name: UserFirstName) -> None:
        first_name_length: int = len(new_first_name)

        if not (
                MIN_TELEGRAM_USERNAME_LENGTH
                <= first_name_length
                <= MAX_TELEGRAM_USERNAME_LENGTH
        ):
            msg: str = (
                f"Length of telegram username must be between"
                f" {MIN_TELEGRAM_USERNAME_LENGTH} and {MAX_TELEGRAM_USERNAME_LENGTH}"
            )
            raise InvalidTelegramUsernameError(msg)

        telegram_user.first_name = new_first_name

        self._record_event(
            TelegramUserUpdatedEvent(
                telegram_id=telegram_user.id,
                first_name=new_first_name.value,
            )
        )

    def change_bot_status(self, telegram_user: TelegramUser, new_status: bool) -> None:
        telegram_user.is_bot = new_status

        self._record_event(
            TelegramUserUpdatedEvent(
                telegram_id=telegram_user.id,
                is_bot=new_status,
            )
        )

    def change_premium_status(self, telegram_user: TelegramUser, new_status: bool) -> None:
        telegram_user.is_premium = new_status

        self._record_event(
            TelegramUserUpdatedEvent(
                telegram_id=telegram_user.id,
                is_premium=new_status,
            )
        )
