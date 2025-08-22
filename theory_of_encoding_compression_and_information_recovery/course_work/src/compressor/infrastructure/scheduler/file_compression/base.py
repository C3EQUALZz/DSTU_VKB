from abc import abstractmethod
from typing import Protocol

from compressor.infrastructure.scheduler.file_compression.contracts import FileInfoDTO
from compressor.infrastructure.scheduler.task_id import TaskID


class FileScheduler(Protocol):
    @abstractmethod
    async def schedule_file_compression(self, dto: FileInfoDTO) -> TaskID:
        ...
