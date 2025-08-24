from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from compressor.domain.files.values.file_id import FileID
from compressor.domain.users.values.user_id import UserID


@dataclass(frozen=True, slots=True, kw_only=True)
class FileForSendInfoDTO:
    file_id: FileID


class Sender(Protocol):
    @abstractmethod
    async def send_file(self, user_id: UserID, file: FileForSendInfoDTO) -> None:
        ...