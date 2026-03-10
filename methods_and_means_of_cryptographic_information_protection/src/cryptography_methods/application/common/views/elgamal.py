"""Views for ElGamal operations."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ElGamalEncryptionView:
    """View for ElGamal encryption result."""

    original_message: str
    ciphertext_pairs_count: int
    output_file: str
    p_bits: int
    g: int
    y_bits: int
    sample_a: int | None
    sample_b: int | None


@dataclass(frozen=True, slots=True)
class ElGamalDecryptionView:
    """View for ElGamal decryption result."""

    decrypted_message: str
    original_message_from_file: str
    ciphertext_pairs_count: int
    input_file: str
    p_bits: int
    x_bits: int


@dataclass(frozen=True, slots=True)
class ElGamalKeyGenerationView:
    """View for ElGamal key generation result."""

    p_bits: int
    p: int
    g: int
    y_bits: int
    y: int
    x_bits: int
    public_key_file: str
    private_key_file: str
    key_size: int
    prime_certainty: int


