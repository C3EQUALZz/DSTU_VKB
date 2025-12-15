"""Command for ElGamal encryption."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.elgamal import ElGamalEncryptionView
from cryptography_methods.domain.elgamal import ElGamalService, ElGamalCiphertext, ElGamalPublicKey

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ElGamalEncryptCommand:
    """Command for ElGamal encryption."""

    message: str
    public_key_file: Path
    output_file: Path


@final
class ElGamalEncryptCommandHandler:
    """Handler for ElGamal encryption command."""

    def __init__(self, elgamal_service: ElGamalService) -> None:
        """Initialize handler.

        Args:
            elgamal_service: ElGamal domain service
        """
        self._service: Final[ElGamalService] = elgamal_service

    async def __call__(self, data: ElGamalEncryptCommand) -> ElGamalEncryptionView:
        """Execute ElGamal encryption command.

        Args:
            data: Encryption command data

        Returns:
            Encryption view with results
        """
        logger.info(
            "Starting ElGamal encryption. Message length: %s, public_key_file=%s, output_file=%s",
            len(data.message),
            data.public_key_file,
            data.output_file,
        )

        # 1. Загрузка публичного ключа
        logger.info("Loading ElGamal public key from: %s", data.public_key_file)
        public_key: ElGamalPublicKey = self._service.load_public_key(data.public_key_file)

        # 2. Шифрование сообщения
        message_bytes: bytes = data.message.encode("utf-8")
        logger.info("Encrypting %s bytes with ElGamal", len(message_bytes))

        ciphertext: list[ElGamalCiphertext] = self._service.encrypt_bytes(
            message=message_bytes,
            public_key=public_key,
        )

        logger.info("Message encrypted successfully. Ciphertext pairs: %s", len(ciphertext))

        # 3. Сохранение в файл шифртекста (отдельно от ключей):
        # original_message
        # a b
        # a b
        logger.info("Saving ElGamal ciphertext to file: %s", data.output_file)
        self._save_ciphertext(
            output_file=data.output_file,
            ciphertext=ciphertext,
        )
        logger.info("ElGamal ciphertext saved successfully")

        return ElGamalEncryptionView(
            original_message=data.message,
            ciphertext_pairs_count=len(ciphertext),
            output_file=str(data.output_file),
            p_bits=public_key.p.bit_length(),
        )

    def _save_ciphertext(
        self,
        output_file: Path,
        ciphertext: list[ElGamalCiphertext],
    ) -> None:
        """Save ElGamal ciphertext to file.

        Формат файла:
            a b
            a b
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", encoding="utf-8") as f:

            for pair in ciphertext:
                f.write(f"{pair.a} {pair.b}\n")


