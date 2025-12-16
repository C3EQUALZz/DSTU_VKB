"""Command for RSA signature key generation."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.rsa_signature import RSASignatureKeyGenerationView
from cryptography_methods.domain.rsa_signature import RSASignatureService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSASignatureGenerateKeysCommand:
    """Command for generating RSA signature keys."""

    public_key_file: Path
    private_key_file: Path
    key_size: int = 2048
    min_prime_diff_bits: int = 64


@final
class RSASignatureGenerateKeysCommandHandler:
    """Handler for RSA signature key generation command."""

    def __init__(self, rsa_signature_service: RSASignatureService) -> None:
        self._service: Final[RSASignatureService] = rsa_signature_service

    async def __call__(self, data: RSASignatureGenerateKeysCommand) -> RSASignatureKeyGenerationView:
        """Execute RSA signature key generation command."""
        if data.key_size <= 0:
            msg = f"Key size must be positive, got {data.key_size}"
            logger.error(msg)
            raise ValueError(msg)

        if data.min_prime_diff_bits <= 0:
            msg = f"min_prime_diff_bits must be positive, got {data.min_prime_diff_bits}"
            logger.error(msg)
            raise ValueError(msg)

        logger.info(
            "Starting RSA signature key generation: key_size=%s, min_prime_diff_bits=%s",
            data.key_size,
            data.min_prime_diff_bits,
        )
        logger.info("Public key will be saved to: %s", data.public_key_file)
        logger.info("Private key will be saved to: %s", data.private_key_file)

        key_pair = self._service.generate_key_pair(
            key_size=data.key_size,
            min_prime_diff_bits=data.min_prime_diff_bits,
        )

        # Save keys
        self._service.save_public_key(key_pair.public_key, data.public_key_file)
        self._service.save_private_key(key_pair.private_key, data.private_key_file)

        logger.info("RSA signature keys saved successfully")

        return RSASignatureKeyGenerationView(
            key_size=data.key_size,
            min_prime_diff_bits=data.min_prime_diff_bits,
            n_bits=key_pair.public_key.n.bit_length(),
            public_key_file=str(data.public_key_file),
            private_key_file=str(data.private_key_file),
        )


