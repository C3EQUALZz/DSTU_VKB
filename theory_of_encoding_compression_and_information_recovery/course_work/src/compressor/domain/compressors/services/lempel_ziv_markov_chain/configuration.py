from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LZMAConfiguration:
    CHUNK_SIZE: int = 8192
    COMPRESS_LEVEL: int = 6
