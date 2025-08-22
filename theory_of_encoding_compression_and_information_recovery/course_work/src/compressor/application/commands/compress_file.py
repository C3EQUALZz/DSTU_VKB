from dataclasses import dataclass
from pathlib import Path
from typing import final, Final

from compressor.application.common.views.compress_file import CompressFileView
from compressor.domain.compressors.services.factory import CompressorType
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.infrastructure.scheduler.file_compression.base import FileScheduler
from compressor.infrastructure.scheduler.file_compression.contracts import FileInfoDTO
from compressor.infrastructure.scheduler.task_id import TaskID


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressFileCommand:
    compressor_type: str
    path: Path


@final
class CompressFileCommandHandler:
    def __init__(
            self,
            file_scheduler: FileScheduler,
            file_service: FileService,
    ) -> None:
        self._file_scheduler: Final[FileScheduler] = file_scheduler
        self._file_service: Final[FileService] = file_service

    async def __call__(self, data: CompressFileCommand) -> CompressFileView:
        new_file: File = self._file_service.create(path=data.path)

        new_task: TaskID = await self._file_scheduler.schedule_file_compression(
            dto=FileInfoDTO(
                file_id=new_file.id,
                compressor_type=CompressorType(data.compressor_type),
            )
        )

        return CompressFileView(
            task_id=new_task,
        )
