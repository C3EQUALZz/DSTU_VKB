import logging
from pathlib import Path

from app.domain.entities.file_objects import CompressedFileObjectEntity
from app.infrastructure.repositories.database.base import \
    DatabaseDumpRepository

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self, repository: DatabaseDumpRepository) -> None:
        self._repository = repository

    def add(self, model: CompressedFileObjectEntity, delete: bool = True) -> None:
        self._repository.add(model)
        logger.info(f"Added {model}")
        if delete:
            Path.unlink(model.file_path)
            logger.info(f"Deleted {model.file_path}")

    def delete(self, oid: str) -> None:
        self._repository.delete(oid)
        logger.info(f"Deleted {oid}")

    def get(self, oid: str) -> None:
        file_from_s3: CompressedFileObjectEntity = self._repository.get(oid)
        logger.info("File downloaded: %s", file_from_s3.file_path)

    def list(self, start: int | None = None, end: int | None = None) -> None:
        files_from_s3: list[CompressedFileObjectEntity] = self._repository.list(start, end)
        logger.info("Files on s3: %s", len(files_from_s3))
