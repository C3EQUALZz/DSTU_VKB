"""VigenereCipher — модифицированный шифр Виженера по байтам (mod 256).

Шифрует поток байтов сообщения путём посимвольного сложения с потоком
байтов ключа, циклически повторяемого. Дешифрование — вычитание.
"""

from typing import final

from steganography.domain.lsb_bmp_vigenere.errors.lsb_errors import (
    EmptyKeyError,
)


@final
class VigenereCipher:
    """Симметричное шифрование байтового потока на основе ключа."""

    def encrypt(self, data: bytes, key: str) -> bytes:
        key_bytes = self._key_bytes(key)
        return bytes(
            (byte + key_bytes[index % len(key_bytes)]) % 256
            for index, byte in enumerate(data)
        )

    def decrypt(self, data: bytes, key: str) -> bytes:
        key_bytes = self._key_bytes(key)
        return bytes(
            (byte - key_bytes[index % len(key_bytes)]) % 256
            for index, byte in enumerate(data)
        )

    def _key_bytes(self, key: str) -> bytes:
        encoded = key.encode("utf-8")
        if not encoded:
            raise EmptyKeyError
        return encoded
