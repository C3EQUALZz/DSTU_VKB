from dataclasses import dataclass
from pathlib import Path
from typing import final, Final

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
class TextFileCompressionTaskCommand:
    compressor_type: str
    path: Path


@final
class TextFileCompressionTaskCommandHandler:
    def __init__(
            self,
            file_scheduler: TextFileTaskManager,
            file_service: FileService,
            id_provider: IdentityProvider
    ) -> None:
        self._file_scheduler: Final[TextFileTaskManager] = file_scheduler
        self._file_service: Final[FileService] = file_service
        self._id_provider: Final[IdentityProvider] = id_provider

    async def __call__(self, data: TextFileCompressionTaskCommand) -> TaskView:
        new_file: File = self._file_service.create(path=data.path)
        current_user_id: UserID = await self._id_provider.get_current_user_id()

        new_task: TaskID = await self._file_scheduler.compress_and_send_file(
            dto=FileInfoDTO(
                file_id=new_file.id,
                compressor_type=CompressorType(data.compressor_type),
                user_id=current_user_id
            )
        )

        return TaskView(task_id=new_task)
