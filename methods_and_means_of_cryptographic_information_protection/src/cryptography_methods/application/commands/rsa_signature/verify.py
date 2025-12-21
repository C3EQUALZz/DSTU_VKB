"""Command for verifying RSA digital signatures."""
import base64
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from cryptography_methods.application.common.views.rsa_signature import RSASignatureVerifyView
from cryptography_methods.domain.rsa_signature import RSASignatureService, RSASignaturePublicKey

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSASignatureVerifyCommand:
    """Command for RSA digital signature verification."""

    document_path: Path
    signature_file: Path
    public_key_file: Path


@final
class RSASignatureVerifyCommandHandler:
    """Handler for RSA digital signature verification."""

    def __init__(self, rsa_signature_service: RSASignatureService) -> None:
        self._service: Final[RSASignatureService] = rsa_signature_service

    async def __call__(self, data: RSASignatureVerifyCommand) -> RSASignatureVerifyView:
        """Execute RSA digital signature verification."""
        document_path = data.document_path
        signature_path = data.signature_file
        public_key_path = data.public_key_file

        if not document_path.exists():
            msg = f"Document file not found: {document_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        if not signature_path.exists():
            msg = f"Signature file not found: {signature_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        logger.info("Starting RSA signature verification")
        logger.info("Document: %s", document_path)
        logger.info("Signature file: %s", signature_path)
        logger.info("Public key file: %s", public_key_path)

        # 1. Read document
        data_bytes = document_path.read_bytes()
        logger.info("Read %s bytes from document", len(data_bytes))

        # 2. Compute hash
        logger.info("Computing SHA-256 hash of document")
        hash_bytes = self._service.compute_hash(data_bytes)
        hash_hex = hash_bytes.hex()
        logger.info("Document hash (SHA-256): %s", hash_hex)

        # 3. Load signature
        signature_b64 = signature_path.read_text(encoding="utf-8").strip()
        try:
            signature_bytes = base64.b64decode(signature_b64, validate=True)
        except (ValueError, base64.binascii.Error) as exc:
            msg = f"Invalid signature file format (expected base64): {signature_path}"
            logger.error(msg)
            raise ValueError(msg) from exc

        # 4. Load public key
        public_key: RSASignaturePublicKey = self._service.load_public_key(public_key_path)
        logger.info(
            "Loaded RSA signature public key (n_bits=%s, e_bits=%s)",
            public_key.n.bit_length(),
            public_key.e.bit_length(),
        )

        # 5. Verify signature
        logger.info("Verifying RSA signature")
        is_valid = self._service.verify_signature(hash_bytes, signature_bytes, public_key)

        return RSASignatureVerifyView(
            document_path=str(document_path),
            signature_file=str(signature_path),
            key_file=str(public_key_path),
            hash_hex=hash_hex,
            is_valid=is_valid,
        )



