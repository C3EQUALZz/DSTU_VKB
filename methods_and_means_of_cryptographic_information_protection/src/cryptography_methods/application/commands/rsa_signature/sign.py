"""Command for signing documents with RSA digital signature."""
import base64
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.rsa_signature import RSASignatureSignView
from cryptography_methods.domain.rsa_signature import RSASignatureService, RSASignaturePrivateKey

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSASignatureSignCommand:
    """Command for RSA digital signature creation."""

    document_path: Path
    private_key_file: Path
    signature_file: Path
    hash_file: Path | None = None


@final
class RSASignatureSignCommandHandler:
    """Handler for RSA digital signature creation."""

    def __init__(self, rsa_signature_service: RSASignatureService) -> None:
        self._service: Final[RSASignatureService] = rsa_signature_service

    async def __call__(self, data: RSASignatureSignCommand) -> RSASignatureSignView:
        """Execute RSA digital signature creation."""
        document_path = data.document_path
        private_key_path = data.private_key_file
        signature_path = data.signature_file
        hash_path = data.hash_file or document_path.with_suffix(document_path.suffix + ".sha256.txt")

        if not document_path.exists():
            msg = f"Document file not found: {document_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        logger.info("Starting RSA signature creation for document: %s", document_path)
        logger.info("Using private key from: %s", private_key_path)

        # 1. Read document
        data_bytes = document_path.read_bytes()
        logger.info("Read %s bytes from document", len(data_bytes))

        # 2. Compute hash (SHA-256)
        logger.info("Computing SHA-256 hash of document")
        hash_bytes = self._service.compute_hash(data_bytes)
        hash_hex = hash_bytes.hex()
        logger.info("Document hash (SHA-256): %s", hash_hex)

        # 3. Save hash as hex string
        hash_path.parent.mkdir(parents=True, exist_ok=True)
        hash_path.write_text(hash_hex, encoding="utf-8")
        logger.info("Document hash saved to: %s", hash_path)

        # 4. Load private key and sign hash
        private_key: RSASignaturePrivateKey = self._service.load_private_key(private_key_path)
        logger.info(
            "Loaded RSA signature private key (n_bits=%s, d_bits=%s)",
            private_key.n.bit_length(),
            private_key.d.bit_length(),
        )

        logger.info("Creating RSA signature (PKCS#1 v1.5 over SHA-256)")
        signature_bytes = self._service.sign_hash(hash_bytes, private_key)

        # 5. Save signature as base64 (for compatibility with text files)
        signature_b64 = base64.b64encode(signature_bytes).decode("ascii")
        signature_path.parent.mkdir(parents=True, exist_ok=True)
        signature_path.write_text(signature_b64, encoding="utf-8")
        logger.info("Signature saved to file (base64): %s", signature_path)

        return RSASignatureSignView(
            document_path=str(document_path),
            hash_hex=hash_hex,
            hash_file=str(hash_path),
            signature_file=str(signature_path),
            key_file=str(private_key_path),
        )



