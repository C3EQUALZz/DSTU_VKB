from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class MagicTableEncryptView:
    text: str
    encrypted_text: str
    magic_table: list[list[int]]


@dataclass(frozen=True, slots=True, kw_only=True)
class MagicTableDecryptView:
    text: str
    decrypted_text: str
    magic_table: list[list[int]]
