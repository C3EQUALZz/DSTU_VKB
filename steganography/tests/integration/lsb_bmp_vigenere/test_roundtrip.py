"""Интеграционный тест ПР6: записываем BMP → встраиваем → извлекаем."""

import asyncio
from pathlib import Path

import pytest

from steganography.application.commands.lsb_bmp_vigenere.embed import (
    EmbedLsbBmpCommand,
    EmbedLsbBmpCommandHandler,
)
from steganography.application.commands.lsb_bmp_vigenere.extract import (
    ExtractLsbBmpCommand,
    ExtractLsbBmpCommandHandler,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_embedder import (
    LsbEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_extractor import (
    LsbExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.marker_packager import (
    MarkerPackager,
)
from steganography.domain.lsb_bmp_vigenere.services.secret_embedder import (
    SecretEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.secret_extractor import (
    SecretExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.vigenere_cipher import (
    VigenereCipher,
)
from steganography.infrastructure.bmp.pillow_bmp_reader import PillowBmpReader
from steganography.infrastructure.bmp.pillow_bmp_writer import PillowBmpWriter
from tests.integration.factories.bmp_builder import build_random_bmp


def _embed_handler() -> EmbedLsbBmpCommandHandler:
    return EmbedLsbBmpCommandHandler(
        reader=PillowBmpReader(),
        writer=PillowBmpWriter(),
        embedder=SecretEmbedder(
            cipher=VigenereCipher(),
            packager=MarkerPackager(),
            embedder=LsbEmbedder(),
        ),
    )


def _extract_handler() -> ExtractLsbBmpCommandHandler:
    return ExtractLsbBmpCommandHandler(
        reader=PillowBmpReader(),
        extractor=SecretExtractor(
            cipher=VigenereCipher(),
            packager=MarkerPackager(),
            extractor=LsbExtractor(),
        ),
    )


@pytest.mark.parametrize(
    "secret",
    [
        "Стеганография защищает данные.",
        "Hello, world!",
        "Многострочное сообщение с символами 123 + знаки!",
    ],
)
def test_roundtrip_recovers_message(tmp_path: Path, secret: str) -> None:
    cover = build_random_bmp(tmp_path / "cover.bmp", width=64, height=64)
    output = tmp_path / "stego.bmp"

    asyncio.run(
        _embed_handler()(
            EmbedLsbBmpCommand(
                cover_path=cover,
                output_path=output,
                secret_text=secret,
                key="MyKey-42",
            ),
        ),
    )
    view = asyncio.run(
        _extract_handler()(
            ExtractLsbBmpCommand(container_path=output, key="MyKey-42"),
        ),
    )
    assert view.plaintext == secret
