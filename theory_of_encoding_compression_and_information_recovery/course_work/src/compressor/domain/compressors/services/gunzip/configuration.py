from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GunZipConfiguration:
    CHUNK_SIZE: int = 64 * 1024  # 64KB
