from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Gost28147EncryptionView:
    original_text: str
    encrypted_text_hex: str  # Зашифрованные данные в hex-формате
    key: str


@dataclass(frozen=True, slots=True)
class Gost28147DecryptionView:
    original_text: str
    decrypted_text: str
    key: str

