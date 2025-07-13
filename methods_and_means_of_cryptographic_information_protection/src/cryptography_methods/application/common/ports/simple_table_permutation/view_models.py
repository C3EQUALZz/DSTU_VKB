from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimpleTablePermutationEncryptView:
    original_text: str
    encrypted_text: str
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class SimpleTablePermutationDecryptView:
    original_text: str
    decrypted_text: str
    width: int
    height: int
