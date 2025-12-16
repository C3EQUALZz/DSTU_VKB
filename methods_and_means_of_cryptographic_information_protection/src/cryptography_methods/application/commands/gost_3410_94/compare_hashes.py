"""Command for GOST 3410-94 hash comparison."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.gost_3410_94 import Gost341094CompareHashesView
from cryptography_methods.domain.gost_3410_94 import Gost341094Service

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost341094CompareHashesCommand:
    """Command for comparing GOST 3410-94 hashes."""

    hash_file_1: Path
    hash_file_2: Path


@final
class Gost341094CompareHashesCommandHandler:
    """Handler for GOST 3410-94 hash comparison command."""

    def __init__(self, gost_service: Gost341094Service) -> None:
        """Initialize handler.

        Args:
            gost_service: GOST 3410-94 domain service (unused, but kept for consistency)
        """
        self._service: Final[Gost341094Service] = gost_service

    async def __call__(self, data: Gost341094CompareHashesCommand) -> Gost341094CompareHashesView:
        """Execute GOST 3410-94 hash comparison command.

        Args:
            data: Hash comparison command data

        Returns:
            Hash comparison view with results
        """
        logger.info(
            "Starting GOST 3410-94 hash comparison. hash_file_1=%s, hash_file_2=%s",
            data.hash_file_1,
            data.hash_file_2,
        )

        logger.info("=== Сравнение хешей ===")

        hash_1_str = data.hash_file_1.read_text(encoding="utf-8").strip()
        hash_2_str = data.hash_file_2.read_text(encoding="utf-8").strip()

        hash_1 = int(hash_1_str)
        hash_2 = int(hash_2_str)

        logger.info("Хеш 1: %s", hash_1)
        logger.info("Хеш 2: %s", hash_2)

        are_equal = hash_1 == hash_2
        logger.info("Результат: Хеши %s", "совпадают" if are_equal else "не совпадают")

        return Gost341094CompareHashesView(
            hash_file_1=str(data.hash_file_1),
            hash_file_2=str(data.hash_file_2),
            hash_1=hash_1_str,
            hash_2=hash_2_str,
            are_equal=are_equal,
        )

