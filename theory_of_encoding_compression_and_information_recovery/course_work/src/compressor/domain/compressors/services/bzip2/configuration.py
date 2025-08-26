from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BZip2Configuration:
    CHUNK_SIZE: int = 8192  # Размер чанка по умолчанию
    COMPRESS_LEVEL: int = 6  # Уровень сжатия от 1 до 9 (максимальное сжатие)
