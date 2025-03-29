from datetime import datetime
from pathlib import Path

from app.domain.entities.file_objects import FileStatistic


class FileStatService:

    @staticmethod
    def get_file_full_stat(self, file_path: Path) -> FileStatistic:
        stat = file_path.stat()

        f = FileStatistic(
            name=file_path.name,
            size=stat.st_size,
            
        )

        return {
            "Name": file_path.name,
            "Size": f"{round(stat.st_size / 1024, 2)} KB",
            "Type": "Directory" if file_path.is_dir() else "File",
            "Extension": file_path.suffix,
            "Modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "Created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "Permissions": oct(stat.st_mode)[-3:]
        }
