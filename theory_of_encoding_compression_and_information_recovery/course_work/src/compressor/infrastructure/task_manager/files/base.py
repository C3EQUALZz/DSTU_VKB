from abc import abstractmethod
from typing import Protocol

from compressor.infrastructure.task_manager.files.contracts import FileInfoDTO
from compressor.infrastructure.task_manager.task_id import TaskID


class FileTaskManager(Protocol):
    @abstractmethod
    async def compress_and_send_file(self, dto: FileInfoDTO) -> TaskID:
        ...

    @abstractmethod
    async def decompress_and_send_file(self, dto: FileInfoDTO) -> TaskID:
        ...
