from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DoubleSquareWhitestoneEncryptView:
    text: str
    encrypted_text: str
    key_for_encryption: tuple[list[str], list[str]]


@dataclass(frozen=True, slots=True)
class DoubleSquareWhitestoneDecryptView:
    text: str
    decrypted_text: str
    key_for_decryption: tuple[list[str], list[str]]
