"""Command for RSA key generation."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import final, Final

from cryptography_methods.application.common.views.rsa import RSAKeyGenerationView
from cryptography_methods.domain.rsa.services.rsa_service import RSAService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSAGenerateKeysCommand:
    """Command for RSA key generation."""

    public_key_file: Path
    private_key_file: Path
    key_size: int = 2048
    min_prime_diff_bits: int = 64


@final
class RSAGenerateKeysCommandHandler:
    """Handler for RSA key generation command."""

    def __init__(self, rsa_service: RSAService) -> None:
        """Initialize handler.

        Args:
            rsa_service: RSA service for key generation operations
        """
        self._rsa_service: Final[RSAService] = rsa_service

    async def __call__(self, data: RSAGenerateKeysCommand) -> RSAKeyGenerationView:
        """Execute RSA key generation command.

        Args:
            data: Key generation command data

        Returns:
            Key generation view with results
        """
        logger.info(
            "Starting RSA key pair generation with key_size=%s bits, min_prime_diff_bits=%s",
            data.key_size,
            data.min_prime_diff_bits
        )
        logger.info("Public key will be saved to: %s", data.public_key_file)
        logger.info("Private key will be saved to: %s", data.private_key_file)

        # Generate key pair
        logger.info("Generating RSA key pair...")
        key_pair = self._rsa_service.generate_key_pair(
            key_size=data.key_size,
            min_prime_diff_bits=data.min_prime_diff_bits
        )
        logger.info("Key pair generated with id=%s", key_pair.id)

        # Save keys to files
        logger.info("Saving keys to files...")
        self._rsa_service.save_public_key(key_pair.public_key, data.public_key_file)
        self._rsa_service.save_private_key(key_pair.private_key, data.private_key_file)
        logger.info("Keys saved successfully")

        return RSAKeyGenerationView(
            public_key_e=key_pair.public_key.e,
            public_key_n=key_pair.public_key.n,
            private_key_d=key_pair.private_key.d,
            private_key_n=key_pair.private_key.n,
            public_key_file=str(data.public_key_file),
            private_key_file=str(data.private_key_file),
            key_size=data.key_size,
        )

