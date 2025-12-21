"""Views for GOST 3410-94 operations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Gost341094KeyGenerationView:
    """View for GOST 3410-94 key generation result."""

    key_size: int
    p_bits: int
    q_bits: int
    parameters_file: str
    private_key_file: str
    public_key_file: str


@dataclass(frozen=True, slots=True)
class Gost341094SignView:
    """View for GOST 3410-94 signature creation result."""

    document_path: str
    hash_value: str
    hash_file: str
    signature_file: str
    r: str
    s: str


@dataclass(frozen=True, slots=True)
class Gost341094VerifyView:
    """View for GOST 3410-94 signature verification result."""

    document_path: str
    signature_file: str
    hash_value: str
    is_valid: bool


@dataclass(frozen=True, slots=True)
class Gost341094CompareHashesView:
    """View for GOST 3410-94 hash comparison result."""

    hash_file_1: str
    hash_file_2: str
    hash_1: str
    hash_2: str
    are_equal: bool


