from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SingleKeyPermutationEncryptView:
    original_text: str
    encrypted_text: str
    key: str
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class SingleKeyPermutationDecryptView:
    original_text: str
    decrypted_text: str
    key: str
    width: int
    height: int
