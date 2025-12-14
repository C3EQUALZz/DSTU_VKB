"""Command for RSA decryption."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import final, Final

from cryptography_methods.application.common.views.rsa import RSADecryptionView
from cryptography_methods.domain.rsa.services.rsa_service import RSAService
from cryptography_methods.domain.rsa.values.rsa_key import RSAPrivateKey

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSADecryptCommand:
    """Command for RSA decryption."""

    private_key_file: Path
    encrypted_data_file: Path


@final
class RSADecryptCommandHandler:
    """Handler for RSA decryption command."""

    def __init__(self, rsa_service: RSAService) -> None:
        """Initialize handler.

        Args:
            rsa_service: RSA service for decryption operations
        """
        self._rsa_service: Final[RSAService] = rsa_service

    async def __call__(self, data: RSADecryptCommand) -> RSADecryptionView:
        """Execute RSA decryption command.

        Args:
            data: Decryption command data

        Returns:
            Decryption view with results
        """
        logger.info("Starting RSA decryption")
        logger.info("Loading private key from: %s", data.private_key_file)
        logger.info("Loading encrypted data from: %s", data.encrypted_data_file)

        # Load private key
        private_key = self._rsa_service.load_private_key(data.private_key_file)
        logger.info(
            "Private key loaded: d (%s bits), n (%s bits)",
            private_key.d.bit_length(),
            private_key.n.bit_length()
        )

        # Load encrypted data
        logger.info("Loading encrypted data from file...")
        encrypted = self._load_encrypted_data(data.encrypted_data_file)
        logger.info("Encrypted blocks count: %s", len(encrypted))

        # Decrypt message
        logger.info("Decrypting message...")
        decrypted_message = self._rsa_service.decrypt(encrypted, private_key)
        logger.info("Message decrypted successfully. Length: %s", len(decrypted_message))

        return RSADecryptionView(
            decrypted_message=decrypted_message,
            encrypted_blocks=encrypted,
        )

    def _load_encrypted_data(self, file_path: Path) -> list[int]:
        """Load encrypted data from file.

        Args:
            file_path: Path to load file from

        Returns:
            List of encrypted blocks
        """
        logger.debug("Reading encrypted data from file: %s", file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Encrypted data file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            return []

        encrypted = [int(block) for block in content.split()]
        logger.debug("File read successfully. Encrypted blocks: %s", len(encrypted))

        return encrypted

