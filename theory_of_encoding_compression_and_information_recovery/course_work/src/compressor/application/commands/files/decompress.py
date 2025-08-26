from dataclasses import dataclass
from io import BytesIO
from typing import final, Final

from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.storage import FileStorage
from compressor.domain.files.services.file_service import FileService
from compressor.infrastructure.task_manager.files.base import FileTaskManager


@dataclass(frozen=True, slots=True, kw_only=True)
class DecompressFileCommand:
    compressor_type: str
    data: BytesIO
    file_name: str


@final
class DecompressFileCommandHandler:
    def __init__(
            self,
            file_scheduler: FileTaskManager,
            file_service: FileService,
            file_storage: FileStorage,
            id_provider: IdentityProvider
    ) -> None:
        self._file_scheduler: Final[FileTaskManager] = file_scheduler
        self._file_service: Final[FileService] = file_service
        self._file_storage: Final[FileStorage] = file_storage
        self._id_provider: Final[IdentityProvider] = id_provider

    async def __call__(self, data: DecompressFileCommand):
        ...
