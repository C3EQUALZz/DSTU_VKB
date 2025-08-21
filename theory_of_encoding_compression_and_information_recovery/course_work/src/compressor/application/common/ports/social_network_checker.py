from abc import abstractmethod
from typing import Protocol

from compressor.application.common.contracts.telegram_contacts import TelegramContactsData


class SocialNetworkChecker(Protocol):
    @abstractmethod
    async def check_telegram_data(self, telegram_id: int) -> TelegramContactsData | None:
        raise NotImplementedError
