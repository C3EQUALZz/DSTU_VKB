"""Views for RSA operations."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RSAEncryptionView:
    """View for RSA encryption result."""

    encrypted_blocks: list[int]
    public_key_e: int
    public_key_n: int
    private_key_d: int
    private_key_n: int
    message: str


@dataclass(frozen=True, slots=True)
class RSADecryptionView:
    """View for RSA decryption result."""

    decrypted_message: str
    encrypted_blocks: list[int]


@dataclass(frozen=True, slots=True)
class RSAKeyGenerationView:
    """View for RSA key generation result."""

    public_key_e: int
    public_key_n: int
    private_key_d: int
    private_key_n: int
    public_key_file: str
    private_key_file: str
    key_size: int