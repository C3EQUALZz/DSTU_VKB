from pathlib import Path

from app.domain.entities.file_objects import CompressedFileObjectEntity
from app.domain.values.backup import CompressionType
from app.infrastructure.services.s3 import S3Service
from app.logic.commands.s3 import (
    CreateFileInS3Command,
    ListFilesInS3Command,
)
from app.logic.handlers.s3.base import S3CommandHandler


class CreateFileInS3CommandHandler(S3CommandHandler[CreateFileInS3Command]):
    def __call__(self, command: CreateFileInS3Command) -> None:
        s3_service: S3Service = S3Service(self._repository)

        file_path: Path = Path(command.file_path)

        file_obj: CompressedFileObjectEntity = CompressedFileObjectEntity(
            file_path=file_path,
            compression_type=CompressionType(file_path.suffix)
        )

        s3_service.add(model=file_obj, delete=command.delete)


class ListFilesInS3CommandHandler(S3CommandHandler[ListFilesInS3Command]):
    def __call__(self, command: ListFilesInS3Command) -> None:
        s3_service: S3Service = S3Service(self._repository)
        s3_service.list(start=command.start, end=command.end)
