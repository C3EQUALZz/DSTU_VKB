"""Тесты ASCII-кодировки."""

import pytest

from steganography.domain.common.encodings.ascii_encoding import (
    AsciiEncoding,
)


@pytest.fixture
def ascii_encoding() -> AsciiEncoding:
    return AsciiEncoding()


def test_decodes_latin(ascii_encoding: AsciiEncoding) -> None:
    bits = "".join(f"{b:08b}" for b in b"Hello")
    assert ascii_encoding.decode(bits) == "Hello"


def test_rejects_non_ascii_bytes(ascii_encoding: AsciiEncoding) -> None:
    # 0xFF выходит за пределы ASCII (>0x7F) — должно вернуть None
    assert ascii_encoding.decode("11111111") is None


def test_empty_input_returns_none(ascii_encoding: AsciiEncoding) -> None:
    assert ascii_encoding.decode("") is None


def test_encode_then_decode_is_identity(
    ascii_encoding: AsciiEncoding,
) -> None:
    bits = ascii_encoding.encode("Hello, world!")
    assert bits is not None
    assert ascii_encoding.decode(bits) == "Hello, world!"


def test_encode_rejects_non_ascii(ascii_encoding: AsciiEncoding) -> None:
    assert ascii_encoding.encode("привет") is None
