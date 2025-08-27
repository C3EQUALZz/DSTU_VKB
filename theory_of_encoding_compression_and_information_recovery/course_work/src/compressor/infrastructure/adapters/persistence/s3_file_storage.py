import logging
from io import BytesIO
from typing import Any, Final

from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError, EndpointConnectionError
from typing_extensions import override

from compressor.application.common.ports.storage import FileStorage, FileStorageDTO
from compressor.domain.files.values.file_id import FileID
from compressor.domain.files.values.file_name import FileName
from compressor.infrastructure.adapters.persistence.constants import (
    DELETE_FILE_FAILED,
    DOWNLOAD_FILE_FAILED,
    UPLOAD_FILE_FAILED,
)
from compressor.infrastructure.errors.file_storage import FileStorageError

logger: Final[logging.Logger] = logging.getLogger(__name__)


class S3FileStorage(FileStorage):
    def __init__(self, client: AioBaseClient) -> None:
        self._client: Final[AioBaseClient] = client
        self._bucket_name: Final[str] = "files"

    @override
    async def add(self, dto: FileStorageDTO) -> None:
        s3_key: str = f"files/{dto.file_id!s}"

        logger.info("Build s3 key for storage: %s", s3_key)

        dto.data.seek(0)

        try:
            logger.info("Started uploading file: %s", s3_key)
            await self._client.upload_fileobj(
                dto.data,
                self._bucket_name,
                s3_key,
                ExtraArgs={
                    "Metadata": {"original_filename": dto.name.value},
                    "ContentType": "application/octet-stream",  # Можно определить по расширению файла
                },
            )
            logger.info("Finished uploading file: %s", s3_key)

            dto.data.flush()
            dto.data.seek(0)
            dto.data.close()

        except EndpointConnectionError as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

        except ClientError as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

        except Exception as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

    @override
    async def read_by_id(self, file_id: FileID) -> FileStorageDTO | None:
        s3_key: str = f"files/{file_id}"

        try:
            response = await self._client.get_object(Bucket=self._bucket_name, Key=s3_key)
            metadata: dict[str, Any] = response.get("Metadata", {})
            original_filename: str = metadata.get("original_filename", s3_key.split("/")[-1])

            file_data = BytesIO(await response["Body"].read())
            file_data.seek(0)

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.warning("File not found in S3: %s", s3_key)
                return None
            logger.exception(DOWNLOAD_FILE_FAILED)
            raise FileStorageError(DOWNLOAD_FILE_FAILED) from e
        except EndpointConnectionError as e:
            logger.exception(DOWNLOAD_FILE_FAILED)
            raise FileStorageError(DOWNLOAD_FILE_FAILED) from e
        except Exception as e:
            logger.exception(DOWNLOAD_FILE_FAILED)
            raise FileStorageError(DOWNLOAD_FILE_FAILED) from e
        else:
            return FileStorageDTO(file_id=file_id, name=FileName(original_filename), data=file_data)

    @override
    async def delete_by_id(self, file_id: FileID) -> None:
        s3_key: str = f"files/{file_id}"

        try:
            await self._client.delete_object(Bucket=self._bucket_name, Key=s3_key)
            logger.info("File successfully deleted from S3: %s", s3_key)

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.warning("File not found in S3: %s", s3_key)
                return
            logger.exception(DELETE_FILE_FAILED)
            raise FileStorageError(DELETE_FILE_FAILED) from e
        except EndpointConnectionError as e:
            logger.exception(DELETE_FILE_FAILED)
            raise FileStorageError(DELETE_FILE_FAILED) from e
        except Exception as e:
            logger.exception(DELETE_FILE_FAILED)
            raise FileStorageError(DELETE_FILE_FAILED) from e
