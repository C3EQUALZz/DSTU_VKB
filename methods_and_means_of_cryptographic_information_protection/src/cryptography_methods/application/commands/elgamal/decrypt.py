"""Command for ElGamal decryption."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.elgamal import ElGamalDecryptionView
from cryptography_methods.domain.elgamal import ElGamalService, ElGamalCiphertext

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ElGamalDecryptCommand:
    """Command for ElGamal decryption."""

    private_key_file: Path
    input_file: Path


@final
class ElGamalDecryptCommandHandler:
    """Handler for ElGamal decryption command."""

    def __init__(self, elgamal_service: ElGamalService) -> None:
        """Initialize handler.

        Args:
            elgamal_service: ElGamal domain service
        """
        self._service: Final[ElGamalService] = elgamal_service

    async def __call__(self, data: ElGamalDecryptCommand) -> ElGamalDecryptionView:
        """Execute ElGamal decryption command."""
        logger.info(
            "Starting ElGamal decryption. Private key file: %s, input file: %s",
            data.private_key_file,
            data.input_file,
        )

        p, private_key = self._service.load_private_key(data.private_key_file)
        original_message, ciphertext = self._load_ciphertext(data.input_file)

        logger.info("Loaded ElGamal data: p_bits=%s, ciphertext_pairs=%s", p.bit_length(), len(ciphertext))

        logger.info("Decrypting ElGamal ciphertext...")
        decrypted_bytes: bytes = self._service.decrypt_bytes(
            ciphertext=ciphertext,
            public_modulus_p=p,
            private_key=private_key,
        )

        try:
            decrypted_message: str = decrypted_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            msg = (
                "Decryption produced bytes that are not valid UTF-8. "
                "Most likely the private key file does not match the ciphertext file "
                "or the ciphertext file is corrupted."
            )
            logger.error("%s Error: %s", msg, exc)
            raise ValueError(msg) from exc

        logger.info("Decryption finished. Decrypted length=%s", len(decrypted_message))

        return ElGamalDecryptionView(
            decrypted_message=decrypted_message,
            original_message_from_file=original_message,
            ciphertext_pairs_count=len(ciphertext),
            input_file=str(data.input_file),
        )

    def _load_ciphertext(
        self,
        input_file: Path,
    ) -> tuple[str, list[ElGamalCiphertext]]:
        """Load ElGamal ciphertext and original message from file.

        Формат файла:
            original_message
            a b
            a b
        """
        if not input_file.exists():
            msg = f"File not found: {input_file}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        with input_file.open("r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]

        if not lines:
            msg = "Invalid ElGamal ciphertext file format: file is empty"
            logger.error(msg)
            raise ValueError(msg)

        # В текущей версии файл содержит только пары a b, без исходного сообщения.
        # Оставляем original_message пустой строкой для обратной совместимости View.
        original_message = ""

        ciphertext: list[ElGamalCiphertext] = []
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) != 2:
                msg = f"Invalid ciphertext line format: {line!r}"
                logger.error(msg)
                raise ValueError(msg)
            try:
                a = int(parts[0])
                b = int(parts[1])
            except ValueError as exc:
                msg = f"Invalid ciphertext numbers in line: {line!r}"
                logger.error(msg)
                raise ValueError(msg) from exc
            ciphertext.append(ElGamalCiphertext(a=a, b=b))

        return original_message, ciphertext


