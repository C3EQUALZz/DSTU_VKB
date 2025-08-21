from compressor.domain.common.entities.base_aggregate import BaseAggregateRoot
from compressor.domain.users.entities.user import User
from compressor.domain.users.values.telegram_user_id import TelegramID
from dataclasses import dataclass

from compressor.domain.users.values.username import Username


@dataclass(eq=False, kw_only=True)
class TelegramUser(BaseAggregateRoot[TelegramID]):
    user: User
    telegram_username: Username
