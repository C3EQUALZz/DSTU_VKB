from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from compressor.domain.users.values.user_id import UserID


@dataclass(frozen=True, slots=True, kw_only=True)
class FileForSendInfoDTO:
    path: Path


class Sender(Protocol):
    @abstractmethod
    async def send_file(self, user_id: UserID, file: FileForSendInfoDTO) -> None:
        ...
