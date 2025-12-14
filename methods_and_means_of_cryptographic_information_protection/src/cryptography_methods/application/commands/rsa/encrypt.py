"""Command for RSA encryption."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import final, Final

from cryptography_methods.application.common.views.rsa import RSAEncryptionView
from cryptography_methods.domain.rsa.services.rsa_service import RSAService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSAEncryptCommand:
    """Command for RSA encryption."""

    message: str
    public_key_file: Path
    output_file: Path


@final
class RSAEncryptCommandHandler:
    """Handler for RSA encryption command."""

    def __init__(self, rsa_service: RSAService) -> None:
        """Initialize handler.

        Args:
            rsa_service: RSA service for encryption operations
        """
        self._rsa_service: Final[RSAService] = rsa_service

    async def __call__(self, data: RSAEncryptCommand) -> RSAEncryptionView:
        """Execute RSA encryption command.

        Args:
            data: Encryption command data

        Returns:
            Encryption view with results
        """
        logger.info("Starting RSA encryption. Message length: %s", len(data.message))
        logger.info("Loading public key from: %s", data.public_key_file)

        # Load public key
        public_key = self._rsa_service.load_public_key(data.public_key_file)
        logger.info(
            "Public key loaded: e (%s bits), n (%s bits)",
            public_key.e.bit_length(),
            public_key.n.bit_length()
        )

        # Encrypt message
        logger.info("Encrypting message...")
        encrypted = self._rsa_service.encrypt(data.message, public_key)
        logger.info("Message encrypted successfully. Encrypted blocks: %s", len(encrypted))

        # Save encrypted data to file
        logger.info("Saving encrypted data to file: %s", data.output_file)
        self._save_encrypted_data(encrypted, data.output_file)
        logger.info("Encrypted data saved successfully")

        return RSAEncryptionView(
            encrypted_blocks=encrypted,
            public_key_e=public_key.e,
            public_key_n=public_key.n,
            private_key_d=0,  # Not available during encryption
            private_key_n=public_key.n,
            message=data.message,
        )

    def _save_encrypted_data(
        self,
        encrypted: list[int],
        file_path: Path,
    ) -> None:
        """Save encrypted data to file.

        Args:
            encrypted: Encrypted message blocks
            file_path: Path to save file
        """
        logger.debug("Writing encrypted data to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(" ".join(str(block) for block in encrypted))
            f.write("\n")

        logger.debug("File written successfully")

