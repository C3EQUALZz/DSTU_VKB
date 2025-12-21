"""Views for RSA digital signature operations."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RSASignatureKeyGenerationView:
    """View for RSA signature key generation result."""

    key_size: int
    min_prime_diff_bits: int
    n_bits: int
    public_key_file: str
    private_key_file: str


@dataclass(frozen=True, slots=True)
class RSASignatureSignView:
    """View for RSA document signing."""

    document_path: str
    hash_hex: str
    hash_file: str
    signature_file: str
    key_file: str


@dataclass(frozen=True, slots=True)
class RSASignatureVerifyView:
    """View for RSA signature verification."""

    document_path: str
    signature_file: str
    key_file: str
    hash_hex: str
    is_valid: bool



