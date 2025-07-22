from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CeaserClassicEncryptionView:
    original_text: str
    encrypted_text: str
    key: int


@dataclass(frozen=True, slots=True)
class CeaserClassicDecryptionView:
    original_text: str
    decrypted_text: str
    key: int
