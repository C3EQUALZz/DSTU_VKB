"""Интеграционный тест ПР8: encode → save BMP → load → decode."""

import asyncio
from pathlib import Path

import pytest

from steganography.application.commands.kutter_jordan_bossen.embed import (
    EmbedKjbCommand,
    EmbedKjbCommandHandler,
)
from steganography.application.commands.kutter_jordan_bossen.extract import (
    ExtractKjbCommand,
    ExtractKjbCommandHandler,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_embedder import (
    KjbEmbedder,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_extractor import (
    KjbExtractor,
)
from steganography.domain.kutter_jordan_bossen.services.luminance_calculator import (
    LuminanceCalculator,
)
from steganography.infrastructure.bmp.pillow_bmp_reader import PillowBmpReader
from steganography.infrastructure.bmp.pillow_bmp_writer import PillowBmpWriter
from tests.integration.factories.gradient_bmp_builder import (
    build_gradient_bmp,
)


def _embed_handler() -> EmbedKjbCommandHandler:
    return EmbedKjbCommandHandler(
        reader=PillowBmpReader(),
        writer=PillowBmpWriter(),
        embedder=KjbEmbedder(luminance=LuminanceCalculator()),
    )


def _extract_handler() -> ExtractKjbCommandHandler:
    return ExtractKjbCommandHandler(
        reader=PillowBmpReader(),
        extractor=KjbExtractor(),
    )


@pytest.mark.parametrize(
    "secret",
    ["КДБ работает!", "Привет!", "Hello, world!"],
)
def test_kjb_recovers_message(tmp_path: Path, secret: str) -> None:
    cover = build_gradient_bmp(tmp_path / "cover.bmp", width=128, height=128)
    output = tmp_path / "stego.bmp"

    asyncio.run(
        _embed_handler()(
            EmbedKjbCommand(
                cover_path=cover,
                output_path=output,
                secret_text=secret,
                lambda_factor=0.3,
                seed=7,
            ),
        ),
    )
    view = asyncio.run(
        _extract_handler()(
            ExtractKjbCommand(
                container_path=output, lambda_factor=0.3, seed=7,
            ),
        ),
    )
    assert view.message == secret
