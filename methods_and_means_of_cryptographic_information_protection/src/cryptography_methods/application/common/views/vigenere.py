from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VigenereEncryptView:
    original_text: str
    encrypted_text: str
    key: str
    length_of_alphabet: int


@dataclass(frozen=True, slots=True)
class VigenereDecryptView:
    original_text: str
    decrypted_text: str
    key: str
    length_of_alphabet: int
