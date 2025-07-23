from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AffineSystemOfCeaserSubstitutionEncryptionView:
    original_text: str
    encrypted_text: str
    a: int
    b: int
    m: int


@dataclass(frozen=True, slots=True)
class AffineSystemOfCeaserSubstitutionDecryptionView:
    original_text: str
    decrypted_text: str
    a: int
    b: int
    m: int
