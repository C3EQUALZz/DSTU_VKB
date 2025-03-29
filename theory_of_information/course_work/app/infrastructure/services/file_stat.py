from datetime import datetime
from pathlib import Path

from app.domain.entities.file_objects import FileStatistic
from app.domain.values.file_objects import TypeOfFile, SizeOfFile, PermissionsOfFile


class FileStatService:
    @staticmethod
    def get_file_full_stat(file_path: Path) -> FileStatistic:
        stat = file_path.stat()

        return FileStatistic(
            name=file_path.name,
            size=SizeOfFile(str(stat.st_size)),
            type_of_file=TypeOfFile("Directory" if file_path.is_dir() else "File"),
            extension=file_path.suffix,
            permissions=PermissionsOfFile(oct(stat.st_mode)[-3:]),
            created_at=datetime.fromtimestamp(stat.st_ctime),
            updated_at=datetime.fromtimestamp(stat.st_mtime),
        )
