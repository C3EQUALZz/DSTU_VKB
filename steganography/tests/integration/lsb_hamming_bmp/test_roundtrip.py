"""Интеграционный тест ПР7: три метода через CLI-handler по реальному BMP."""

import asyncio
from pathlib import Path

import pytest

from steganography.application.commands.lsb_hamming_bmp.embed import (
    EmbedLsbHammingCommand,
    EmbedLsbHammingCommandHandler,
)
from steganography.application.commands.lsb_hamming_bmp.extract import (
    ExtractLsbHammingCommand,
    ExtractLsbHammingCommandHandler,
)
from steganography.domain.lsb_hamming_bmp.services.channel_stream import (
    ChannelStream,
)
from steganography.domain.lsb_hamming_bmp.services.hamming_15_11_method import (
    Hamming15_11Method,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_matching_method import (
    LsbMatchingMethod,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_replacement_method import (
    LsbReplacementMethod,
)
from steganography.domain.lsb_hamming_bmp.value_objects.embedding_method import (
    EmbeddingMethod,
)
from steganography.infrastructure.bmp.pillow_bmp_reader import PillowBmpReader
from steganography.infrastructure.bmp.pillow_bmp_writer import PillowBmpWriter
from tests.integration.factories.bmp_builder import build_random_bmp


def _embed_handler() -> EmbedLsbHammingCommandHandler:
    channels = ChannelStream()
    return EmbedLsbHammingCommandHandler(
        reader=PillowBmpReader(),
        writer=PillowBmpWriter(),
        lsb_r=LsbReplacementMethod(channel_stream=channels),
        lsb_m=LsbMatchingMethod(channel_stream=channels, seed=42),
        hamming=Hamming15_11Method(channel_stream=channels),
    )


def _extract_handler() -> ExtractLsbHammingCommandHandler:
    channels = ChannelStream()
    return ExtractLsbHammingCommandHandler(
        reader=PillowBmpReader(),
        lsb_r=LsbReplacementMethod(channel_stream=channels),
        lsb_m=LsbMatchingMethod(channel_stream=channels, seed=42),
        hamming=Hamming15_11Method(channel_stream=channels),
    )


@pytest.mark.parametrize(
    ("method", "secret"),
    [
        (EmbeddingMethod.LSB_REPLACEMENT, "LSB-R сообщение"),
        (EmbeddingMethod.LSB_MATCHING, "LSB-M сообщение"),
        (EmbeddingMethod.HAMMING_15_11, "Хемминг (15,11)"),
    ],
)
def test_method_roundtrip(
    tmp_path: Path, method: EmbeddingMethod, secret: str,
) -> None:
    cover = build_random_bmp(tmp_path / "cover.bmp", width=64, height=64)
    output = tmp_path / "stego.bmp"

    asyncio.run(
        _embed_handler()(
            EmbedLsbHammingCommand(
                cover_path=cover,
                output_path=output,
                secret_text=secret,
                method=method,
                step=1,
            ),
        ),
    )
    view = asyncio.run(
        _extract_handler()(
            ExtractLsbHammingCommand(
                container_path=output,
                method=method,
                step=1,
            ),
        ),
    )
    assert view.message == secret
