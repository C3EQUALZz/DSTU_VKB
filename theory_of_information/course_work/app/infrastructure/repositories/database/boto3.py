import logging
from pathlib import Path
from typing import Any

from botocore.exceptions import ClientError
from typing_extensions import override

from app.application.cli.const import BACKUP_DIRECTORY_PATH
from app.domain.entities.file_objects import CompressedFileObject
from app.domain.values.backup import CompressionType
from app.infrastructure.repositories.base import S3AbstractRepository
from app.infrastructure.repositories.database.base import DatabaseDumpRepository

logger = logging.getLogger(__name__)


class DatabaseDumpBoto3Repository(DatabaseDumpRepository, S3AbstractRepository):
    @override
    def add(self, model: CompressedFileObject) -> CompressedFileObject:
        object_key = self._generate_object_key(model.file_path.name)

        try:
            self._client.upload_file(
                Filename=str(model.file_path),
                Bucket=self._bucket_name,
                Key=object_key,
                ExtraArgs={
                    "Metadata": {
                        "compression": model.compression_type.as_generic_type(),
                        "original_filename": model.file_path.name,
                        "oid": model.oid,
                    }
                }
            )
            logger.info(f"Uploaded {object_key} to {self._bucket_name}")

            return CompressedFileObject(
                file_path=Path(object_key),
                compression_type=model.compression_type
            )

        except ClientError as e:
            logger.error(f"Upload failed: {e}")
            raise

    @override
    def get(self, oid: str) -> CompressedFileObject | None:
        try:

            head_response: dict[str, Any] = self._client.head_object(
                Bucket=self._bucket_name,
                Key=oid
            )

            # Извлекаем тип сжатия из метаданных
            metadata: dict[str, str] = head_response.get("Metadata", {})
            compression_type_str: str = metadata.get("compression", "unknown")
            name = metadata.get("original_filename", "unknown")

            local_path = BACKUP_DIRECTORY_PATH / name

            self._client.download_file(
                Bucket=self._bucket_name,
                Key=oid,
                Filename=str(local_path)
            )

            return CompressedFileObject(
                file_path=local_path,
                compression_type=CompressionType(compression_type_str)  # Определите тип из метаданных
            )

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.warning(f"Object {oid} not found")
                return None
            logger.error(f"Download failed: {e}")
            raise

    @override
    def update(self, oid: str, model: CompressedFileObject) -> CompressedFileObject:
        raise NotImplementedError

    @override
    def list(
            self,
            start: int | None = None,
            limit: int | None = None
    ) -> list[CompressedFileObject]:
        result: list[CompressedFileObject] = []
        paginator = self._client.get_paginator("list_objects_v2")

        config = {
            "Bucket": self._bucket_name,
            "Prefix": self._bucket_path,
            "MaxKeys": limit or 1000
        }

        if start:
            config["ContinuationToken"] = str(start)

        try:
            for page in paginator.paginate(**config):
                for obj in page.get("Contents", []):
                    # Получаем полные метаданные для каждого объекта
                    metadata = self._get_object_metadata(obj["Key"])
                    result.append(
                        CompressedFileObject(
                            file_path=Path(obj["Key"]),
                            compression_type=metadata.get("compression")
                        )
                    )

                    if limit and len(result) >= limit:
                        return result
            return result

        except ClientError as e:
            logger.error(f"Listing failed: {e}")
            raise

    def _get_object_metadata(self, key: str) -> dict:
        """Получение метаданных объекта через head_object"""
        try:
            response = self._client.head_object(
                Bucket=self._bucket_name,
                Key=key
            )
            return response.get("Metadata", {})

        except ClientError as e:
            logger.warning(f"Metadata fetch failed for {key}: {e}")
            return {}

    @override
    def delete(self, oid: str) -> None:
        try:
            self._client.delete_object(
                Bucket=self._bucket_name,
                Key=oid
            )
            logger.info(f"Deleted object {oid}")

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.warning(f"Object {oid} not found")
                return
            logger.error(f"Delete failed: {e}")
            raise

    def _generate_object_key(self, filename: str) -> str:
        """Generate S3 object key"""
        return f"{self._bucket_path}{filename}"
