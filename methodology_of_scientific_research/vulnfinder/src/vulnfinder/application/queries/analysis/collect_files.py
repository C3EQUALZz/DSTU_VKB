from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class CollectFilesQuery:
    path: Path
    recursive: bool | None = None
    extensions: tuple[str, ...] = ()


class CollectFilesQueryHandler:
    def __call__(self, data: CollectFilesQuery) -> list[Path]:
        if data.path.is_file():
            return [data.path]

        recursive = bool(data.recursive)
        pattern = "**/*" if recursive else "*"
        results = [entry for entry in data.path.glob(pattern) if entry.is_file()]
        if data.extensions:
            results = [
                entry for entry in results if entry.suffix.lower() in data.extensions
            ]
        return results
