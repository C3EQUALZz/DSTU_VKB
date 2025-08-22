import hashlib
from pathlib import Path
from typing import cast

from compressor.domain.files.ports.file_id_generator import FileIDGenerator
from compressor.domain.files.values.file_id import FileID


class FileSha256IDGenerator(FileIDGenerator):
    def __call__(self, path: Path) -> FileID:
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            for block in iter(lambda: f.read(65536), b''):
                sha256.update(block)
        return cast(FileID, sha256.hexdigest())
