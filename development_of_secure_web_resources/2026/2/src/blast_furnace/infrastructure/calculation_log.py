import fcntl
from datetime import datetime
from pathlib import Path

from blast_furnace.domain.temperature import BlastParameters


class FileCalculationLog:
    def __init__(self, path: Path) -> None:
        self._path = path

    def append(self, parameters: BlastParameters, result: float, comment: str) -> None:
        # Экранируем разделители: пользователь не может подделать новую запись.
        comment = (
            comment.replace("\\", "\\\\")
            .replace("\r", "\\r")
            .replace("\n", "\\n")
            .replace("|", "\\|")
        )
        line = (
            f"{datetime.now().astimezone().isoformat(timespec='seconds')} | "
            f"Тд={parameters.t_blast:g} Wд={parameters.humidity:g} "
            f"w={parameters.oxygen:g} Vпг={parameters.gas:g} | "
            f"Тг={result:.1f} | {comment}\n"
        )
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            stream.write(line)
            stream.flush()
            # Закрытие файла освобождает блокировку, в том числе при исключении.
