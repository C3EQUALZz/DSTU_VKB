"""Command for GOST 3410-94 key generation."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.gost_3410_94 import Gost341094KeyGenerationView
from cryptography_methods.domain.gost_3410_94 import Gost341094Service

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost341094GenerateKeysCommand:
    """Command for generating GOST 3410-94 keys."""

    parameters_file: Path
    private_key_file: Path
    public_key_file: Path
    key_size: int = 512


@final
class Gost341094GenerateKeysCommandHandler:
    """Handler for GOST 3410-94 key generation command."""

    def __init__(self, gost_service: Gost341094Service) -> None:
        """Initialize handler.

        Args:
            gost_service: GOST 3410-94 domain service
        """
        self._service: Final[Gost341094Service] = gost_service

    async def __call__(self, data: Gost341094GenerateKeysCommand) -> Gost341094KeyGenerationView:
        """Execute GOST 3410-94 key generation command.

        Args:
            data: Key generation command data

        Returns:
            Key generation view with results
        """
        logger.info(
            "Starting GOST 3410-94 key generation. key_size=%s, parameters_file=%s, private_key_file=%s, public_key_file=%s",
            data.key_size,
            data.parameters_file,
            data.private_key_file,
            data.public_key_file,
        )

        key_pair = self._service.generate_parameters_and_keys(key_size=data.key_size)

        self._service.save_parameters_and_keys(
            key_pair=key_pair,
            parameters_file=data.parameters_file,
            private_key_file=data.private_key_file,
            public_key_file=data.public_key_file,
        )

        logger.info("GOST 3410-94 keys generated and saved successfully")

        return Gost341094KeyGenerationView(
            key_size=data.key_size,
            p_bits=key_pair.parameters.p.bit_length(),
            q_bits=key_pair.parameters.q.bit_length(),
            parameters_file=str(data.parameters_file),
            private_key_file=str(data.private_key_file),
            public_key_file=str(data.public_key_file),
        )

