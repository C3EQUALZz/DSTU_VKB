"""
Configuration values for the pgzip module.
"""

import os
from typing import Final


class Configuration:
    """
    The configuration values for executing the algorithm, as they are defined inside
    the original files.
    """

    # Определение числа доступных ядер процессора.
    CPU_COUNT: Final[int] = os.cpu_count() if os.cpu_count() is not None else 6  # type: ignore[assignment]

    # Размер блока для сжатия (в килобайтах).
    DEFAULT_BLOCK_SIZE_KB: Final[int] = 128

    # Опции уровня сжатия для gzip: 1 — самый быстрый, 9 — самый эффективный.
    GZIP_COMPRESS_OPTIONS: Final[list[int]] = list(range(1, 10))

    COMPRESS_LEVEL_BEST: Final[int] = max(GZIP_COMPRESS_OPTIONS)

    # Размер чанка для чтения (можно заменить на CHUNK_SIZE, если он отличается).
    # Если CHUNK_SIZE уже определён в другом модуле, его можно импортировать.
    CHUNK_SIZE: Final[int] = 65536

    # FLG bits для gzip заголовка
    FTEXT: Final[int] = 0x1
    FHCRC: Final[int] = 0x2
    FEXTRA: Final[int] = 0x4
    FNAME: Final[int] = 0x8
    FCOMMENT: Final[int] = 0x10
