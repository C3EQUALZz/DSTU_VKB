from dataclasses import dataclass


@dataclass(frozen=True)
class FileWithDimensions:
    data: bytes
    width: int
    height: int
    name: str
