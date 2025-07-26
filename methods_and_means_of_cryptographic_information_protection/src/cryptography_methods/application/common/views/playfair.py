from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlayfairEncryptView:
    original_text: str
    encrypted_text: str
    key: str
    width: int
    height: int
    length_of_alphabet: int


@dataclass(frozen=True, slots=True)
class PlayfairDecryptView:
    original_text: str
    decrypted_text: str
    key: str
    width: int
    height: int
    length_of_alphabet: int