from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import final, Final

from compressor.application.common.ports.file_storage import FileStorageService, FileStorageDTO
from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.views.tasks import TaskView
from compressor.domain.compressors.factories.text.base import CompressorType
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.users.values.user_id import UserID
from compressor.infrastructure.task_manager.task_id import TaskID
from compressor.infrastructure.task_manager.text.base import TextFileTaskManager
from compressor.infrastructure.task_manager.text.contracts import FileInfoDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressFileCommand:
    compressor_type: str
    data: BytesIO
    path: Path


@final
class CompressFileCommandHandler:
    def __init__(
            self,
            file_scheduler: TextFileTaskManager,
            file_service: FileService,
            file_storage: FileStorageService,
            id_provider: IdentityProvider
    ) -> None:
        self._file_storage: Final[FileStorageService] = file_storage
        self._file_scheduler: Final[TextFileTaskManager] = file_scheduler
        self._file_service: Final[FileService] = file_service
        self._id_provider: Final[IdentityProvider] = id_provider

    async def __call__(self, data: CompressFileCommand) -> TaskView:
        current_user_id: UserID = await self._id_provider.get_current_user_id()

        new_file: File = self._file_service.create(path=data.path, data=data.data)

        await self._file_storage.add(
            FileStorageDTO(
                file_id=new_file.id,
                path=new_file.path,
                data=data.data
            )
        )

        new_task: TaskID = await self._file_scheduler.compress_and_send_file(
            dto=FileInfoDTO(
                file_path=new_file.path,
                compressor_type=CompressorType(data.compressor_type),
                user_id=current_user_id,
                file_id=new_file.id
            )
        )

        return TaskView(task_id=new_task)
