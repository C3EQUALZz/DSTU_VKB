"""Тесты обёртки сообщения метками начала/конца."""

import pytest

from steganography.domain.lsb_bmp_vigenere.errors.lsb_errors import (
    MarkersNotFoundError,
)
from steganography.domain.lsb_bmp_vigenere.services.marker_packager import (
    MarkerPackager,
)


@pytest.fixture
def packager() -> MarkerPackager:
    return MarkerPackager()


def test_pack_unpack_roundtrip(packager: MarkerPackager) -> None:
    framed = packager.pack(b"payload")
    assert packager.unpack(framed) == b"payload"


def test_unpack_finds_payload_inside_noise(packager: MarkerPackager) -> None:
    framed = b"AAAAA" + packager.pack(b"abc") + b"BBBBB"
    assert packager.unpack(framed) == b"abc"


def test_unpack_without_markers_raises(packager: MarkerPackager) -> None:
    with pytest.raises(MarkersNotFoundError):
        packager.unpack(b"random noise without markers")
