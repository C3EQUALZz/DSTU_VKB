from dataclasses import dataclass, field

from compressor.domain.common.entities.base_entity import BaseEntity
from compressor.domain.users.values.telegram_user_id import TelegramID
from compressor.domain.users.values.user_first_name import UserFirstName
from compressor.domain.users.values.username import Username


@dataclass(eq=False, kw_only=True)
class TelegramUser(BaseEntity[TelegramID]):
    first_name: UserFirstName
    username: Username | None = None
    last_name: str | None = None
    is_premium: bool = field(default=False)
    is_bot: bool = field(default=False)
