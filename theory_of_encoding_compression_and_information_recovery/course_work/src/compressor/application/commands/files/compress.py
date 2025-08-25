import logging
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import final, Final

from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.application.common.views.tasks import TaskView
from compressor.domain.compressors.factories.text.base import CompressorType
from compressor.domain.files.entities.file import File
from compressor.domain.files.services.file_service import FileService
from compressor.domain.files.values.file_name import FileName
from compressor.domain.users.values.user_id import UserID
from compressor.infrastructure.task_manager.task_id import TaskID
from compressor.infrastructure.task_manager.files.base import FileTaskManager
from compressor.infrastructure.task_manager.files.contracts import FileInfoDTO

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class CompressFileCommand:
    compressor_type: str
    data: BytesIO
    file_name: str


@final
class CompressFileCommandHandler:
    def __init__(
            self,
            file_scheduler: FileTaskManager,
            file_service: FileService,
            file_storage: FileStorage,
            id_provider: IdentityProvider
    ) -> None:
        self._file_storage: Final[FileStorage] = file_storage
        self._file_scheduler: Final[FileTaskManager] = file_scheduler
        self._file_service: Final[FileService] = file_service
        self._id_provider: Final[IdentityProvider] = id_provider

    async def __call__(self, data: CompressFileCommand) -> TaskView:
        logger.info(
            "Started file compression, compressor type: %s, file name: %s",
            data.compressor_type,
            data.file_name
        )

        logger.info("Getting current user id")
        current_user_id: UserID = await self._id_provider.get_current_user_id()
        logger.info("Successfully got current user id: %s", current_user_id)

        logger.info("Creating a new file entity with name: %s", data.file_name)
        new_file: File = self._file_service.create(
            file_name=FileName(data.file_name),
            data=data.data
        )
        logger.info("Successfully created new file entity with name: %s", new_file.file_name)

        logger.info(
            "Starting saving file in file storage, with id: %s and path: %s",
            new_file.id,
            new_file.file_name
        )

        await self._file_storage.add(
            FileStorageDTO(
                file_id=new_file.id,
                name=new_file.file_name,
                data=data.data
            )
        )

        new_task: TaskID = await self._file_scheduler.compress_and_send_file(
            dto=FileInfoDTO(
                file_name=new_file.file_name,
                compressor_type=CompressorType(data.compressor_type),
                user_id=current_user_id,
                file_id=new_file.id
            )
        )

        return TaskView(task_id=new_task)
