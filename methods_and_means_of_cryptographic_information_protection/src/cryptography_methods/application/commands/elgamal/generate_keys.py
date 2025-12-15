"""Command for ElGamal key generation."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.elgamal import ElGamalKeyGenerationView
from cryptography_methods.domain.elgamal import ElGamalService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ElGamalGenerateKeysCommand:
    """Command for ElGamal key generation."""

    public_key_file: Path
    private_key_file: Path
    key_size: int = 1024
    prime_certainty: int = 10


@final
class ElGamalGenerateKeysCommandHandler:
    """Handler for ElGamal key generation command."""

    def __init__(self, elgamal_service: ElGamalService) -> None:
        """Initialize handler.

        Args:
            elgamal_service: ElGamal domain service
        """
        self._service: Final[ElGamalService] = elgamal_service

    async def __call__(self, data: ElGamalGenerateKeysCommand) -> ElGamalKeyGenerationView:
        """Execute ElGamal key generation command."""
        if data.key_size <= 0:
            msg = f"Key size must be positive, got {data.key_size}"
            logger.error(msg)
            raise ValueError(msg)

        if data.prime_certainty <= 0:
            msg = f"Prime certainty must be positive, got {data.prime_certainty}"
            logger.error(msg)
            raise ValueError(msg)

        logger.info(
            "Starting ElGamal key generation: key_size=%s, prime_certainty=%s",
            data.key_size,
            data.prime_certainty,
        )
        logger.info("Public key will be saved to: %s", data.public_key_file)
        logger.info("Private key will be saved to: %s", data.private_key_file)

        public_key, private_key = self._service.generate_keys(
            key_size=data.key_size,
            prime_certainty=data.prime_certainty,
        )

        logger.info(
            "Generated ElGamal keys: p_bits=%s, g=%s, y_bits=%s",
            public_key.p.bit_length(),
            public_key.g,
            public_key.y.bit_length(),
        )

        # Save keys to files
        self._service.save_public_key(public_key, data.public_key_file)
        self._service.save_private_key(public_key.p, private_key, data.private_key_file)

        logger.info("ElGamal keys saved successfully")

        return ElGamalKeyGenerationView(
            p_bits=public_key.p.bit_length(),
            g=public_key.g,
            y_bits=public_key.y.bit_length(),
            public_key_file=str(data.public_key_file),
            private_key_file=str(data.private_key_file),
            key_size=data.key_size,
            prime_certainty=data.prime_certainty,
        )


