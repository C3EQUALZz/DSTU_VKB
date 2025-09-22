from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AtbashEncryptionView:
    language: str
    original_text: str
    encrypted_text: str


@dataclass(frozen=True, slots=True)
class AtbashDecryptionView:
    language: str
    original_text: str
    decrypted_text: str
