from typing import Final

from compressor.domain.common.services.base import DomainService
from compressor.domain.users.constants import (
    MIN_TELEGRAM_ID_VALUE,
    MIN_TELEGRAM_USERNAME_LENGTH,
    MAX_TELEGRAM_USERNAME_LENGTH
)
from compressor.domain.users.entities.telegram_user import TelegramUser
from compressor.domain.users.entities.user import User
from compressor.domain.users.errors import TelegramIDMustBePositiveError, InvalidTelegramUsernameError
from compressor.domain.users.services.user_service import UserService
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_raw_password import UserRawPassword
from compressor.domain.users.values.user_role import UserRole
from compressor.domain.users.values.username import Username


class TelegramService(DomainService):
    def __init__(self, user_service: UserService) -> None:
        super().__init__()
        self._user_service: Final[UserService] = user_service

    def create(
            self,
            telegram_id: TelegramID,
            username: Username,
            raw_password: UserRawPassword,
            role: UserRole = UserRole.USER,
            is_active: bool = True,
    ) -> TelegramUser:
        new_user: User = self._user_service.create(
            username=username,
            raw_password=raw_password,
            role=role,
            is_active=is_active,
        )

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

        return TelegramUser(
            id=telegram_id,
            user=new_user,
            telegram_username=username,
        )

    # noinspection PyMethodMayBeStatic
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
