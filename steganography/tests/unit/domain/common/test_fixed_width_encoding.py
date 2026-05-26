"""Тесты 8-битных кодировок (КОИ-8R, cp866, Windows-1251)."""

import pytest

from steganography.domain.common.encodings.fixed_width_encoding import (
    FixedWidthEncoding,
)


@pytest.mark.parametrize(
    ("name", "codec", "text"),
    [
        ("Windows-1251", "windows-1251", "секрет"),
        ("Windows-1251", "windows-1251", "Один бог забыл - другой поможет."),
        ("КОИ-8R", "koi8-r", "Hello, world!"),
        ("КОИ-8R", "koi8-r", "Стеганография это искусство"),
        ("cp866", "cp866", "Привет"),
        ("cp866", "cp866", "ABCDE 12345"),
    ],
)
def test_decode_roundtrip(name: str, codec: str, text: str) -> None:
    encoding = FixedWidthEncoding(name=name, codec=codec)
    bits = "".join(f"{b:08b}" for b in text.encode(codec))
    assert encoding.decode(bits) == text


@pytest.mark.parametrize(
    ("name", "codec", "text"),
    [
        ("Windows-1251", "windows-1251", "секрет"),
        ("КОИ-8R", "koi8-r", "Hello, world!"),
        ("cp866", "cp866", "Привет 123"),
    ],
)
def test_encode_then_decode_is_identity(
    name: str, codec: str, text: str,
) -> None:
    encoding = FixedWidthEncoding(name=name, codec=codec)
    bits = encoding.encode(text)
    assert bits is not None
    assert encoding.decode(bits) == text


def test_remainder_bits_are_dropped() -> None:
    encoding = FixedWidthEncoding(name="Windows-1251", codec="windows-1251")
    assert encoding.decode("01000001" + "010") == "A"


def test_empty_bits_return_none() -> None:
    encoding = FixedWidthEncoding(name="cp866", codec="cp866")
    assert encoding.decode("") is None


def test_encode_rejects_uncodable_text() -> None:
    encoding = FixedWidthEncoding(name="КОИ-8R", codec="koi8-r")
    # японский символ не кодируется в КОИ-8R
    assert encoding.encode("ひらがな") is None
