"""Тесты модифицированного шифра Виженера."""

import pytest

from steganography.domain.lsb_bmp_vigenere.errors.lsb_errors import (
    EmptyKeyError,
)
from steganography.domain.lsb_bmp_vigenere.services.vigenere_cipher import (
    VigenereCipher,
)


@pytest.fixture
def cipher() -> VigenereCipher:
    return VigenereCipher()


@pytest.mark.parametrize(
    "plaintext",
    [b"hello", b"\xff\x00\x7f", "Сообщение".encode("utf-8")],
)
def test_encrypt_then_decrypt_is_identity(
    cipher: VigenereCipher, plaintext: bytes,
) -> None:
    ciphertext = cipher.encrypt(plaintext, "key123")
    assert cipher.decrypt(ciphertext, "key123") == plaintext


def test_empty_key_raises(cipher: VigenereCipher) -> None:
    with pytest.raises(EmptyKeyError):
        cipher.encrypt(b"data", "")
