from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DoubleSquareWhitestoneEncryptView:
    text: str
    encrypted_text: str
    left_table: list[list[str]]
    right_table: list[list[str]]


@dataclass(frozen=True, slots=True)
class DoubleSquareWhitestoneDecryptView:
    text: str
    decrypted_text: str
    left_table: list[list[str]]
    right_table: list[list[str]]
