"""Тесты 5-битной кодировки МТК-2 (Бодо / ITA2)."""

import pytest

from steganography.domain.common.encodings.baudot_mtk2_encoding import (
    BaudotMtk2Encoding,
)


@pytest.fixture
def mtk2() -> BaudotMtk2Encoding:
    return BaudotMtk2Encoding()


def test_decodes_known_letters(mtk2: BaudotMtk2Encoding) -> None:
    assert mtk2.decode("00100") == " "
    assert mtk2.decode("11000" + "00001") == "AT"


def test_switches_to_figures_mode(mtk2: BaudotMtk2Encoding) -> None:
    # FIGS shift + код «2»
    assert mtk2.decode("11011" + "11001") == "2"


def test_empty_input_returns_none(mtk2: BaudotMtk2Encoding) -> None:
    assert mtk2.decode("") is None


@pytest.mark.parametrize(
    "text",
    ["HELLO WORLD", "STEGANOGRAPHY", "ABCDEFG", "ONE TWO"],
)
def test_encode_then_decode_is_identity(
    mtk2: BaudotMtk2Encoding, text: str,
) -> None:
    bits = mtk2.encode(text)
    assert bits is not None
    assert mtk2.decode(bits) == text.upper()


def test_encode_with_letters_and_figures(mtk2: BaudotMtk2Encoding) -> None:
    bits = mtk2.encode("AB12")
    assert bits is not None
    assert mtk2.decode(bits) == "AB12"


def test_encode_rejects_cyrillic(mtk2: BaudotMtk2Encoding) -> None:
    assert mtk2.encode("привет") is None
