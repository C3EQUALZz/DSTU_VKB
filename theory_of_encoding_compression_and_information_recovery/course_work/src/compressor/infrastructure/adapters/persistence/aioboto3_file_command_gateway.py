import logging
from typing import Final

from aiobotocore.client import AioBaseClient
from botocore.exceptions import EndpointConnectionError, ClientError
from typing_extensions import override

from compressor.application.common.ports.file.file_command_gateway import FileCommandGateway
from compressor.domain.files.entities.file import File
from compressor.domain.files.values.file_id import FileID
from compressor.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from compressor.infrastructure.errors.transaction_manager import RepoError

logger: Final[logging.Logger] = logging.getLogger(__name__)


class AioBoto3FileCommandGateway(FileCommandGateway):
    def __init__(self, client: AioBaseClient) -> None:
        self._client: Final[AioBaseClient] = client
        self._bucket_name: Final[str] = "uncompressed_files_bucket"

    @override
    async def add(self, file: File) -> None:
        path_in_s3_storage: str = f"{file.id}/{file.path.name}"

        try:

            with file.path.open("rb") as file_obj:
                await self._client.upload_fileobj(
                    file_obj,
                    self._bucket_name,
                    path_in_s3_storage
                )

        except EndpointConnectionError as e:
            logger.exception(DB_QUERY_FAILED)
            raise RepoError(DB_QUERY_FAILED) from e

        except ClientError as e:
            logger.exception(DB_QUERY_FAILED)
            raise RepoError(DB_QUERY_FAILED) from e

        except Exception as e:
            logger.exception(DB_QUERY_FAILED)
            raise RepoError(DB_QUERY_FAILED) from e


    @override
    async def read_by_id(self, file_id: FileID) -> File:
        ...
