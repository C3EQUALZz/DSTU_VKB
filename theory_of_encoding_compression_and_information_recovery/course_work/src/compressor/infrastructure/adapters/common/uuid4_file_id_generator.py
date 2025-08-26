from typing import cast
from uuid import uuid4

from typing_extensions import override

from compressor.domain.files.ports.file_id_generator import FileIDGenerator
from compressor.domain.files.values.file_id import FileID


class UUID4FileIDGenerator(FileIDGenerator):
    @override
    def __call__(self) -> FileID:
        return cast("FileID", uuid4())
