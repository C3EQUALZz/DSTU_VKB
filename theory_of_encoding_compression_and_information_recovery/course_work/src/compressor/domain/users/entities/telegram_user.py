from compressor.domain.common.entities.base_aggregate import BaseAggregateRoot
from compressor.domain.users.entities.user import User
from compressor.domain.users.values.telegram_user_id import TelegramID
from dataclasses import dataclass


@dataclass(eq=False, kw_only=True)
class TelegramUser(BaseAggregateRoot[TelegramID]):
    user: User
    telegram_username: str
