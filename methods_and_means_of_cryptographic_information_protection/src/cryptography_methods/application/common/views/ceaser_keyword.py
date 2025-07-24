from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CeaserKeywordEncryptionView:
    original_text: str
    encrypted_text: str
    keyword: str
    k: int
    m: int


@dataclass(frozen=True, slots=True)
class CeaserKeywordDecryptionView:
    original_text: str
    decrypted_text: str
    keyword: str
    k: int
    m: int
