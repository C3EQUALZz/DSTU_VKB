"""Интеграционный прогон детектора по реальным variantXX.docx преподавателя."""

import asyncio
from pathlib import Path

import pytest

from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommand,
    DetectSecretCommandHandler,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from tests.integration.text_format_decode.expected_variants import (
    EXPECTED,
    KNOWN_FAILURES,
)


@pytest.mark.parametrize(("filename", "expected"), sorted(EXPECTED.items()))
def test_real_variant_is_decoded(
    detect_handler: DetectSecretCommandHandler,
    variants_dir: Path,
    filename: str,
    expected: tuple[FormattingParam, str, str],
) -> None:
    docx_path = variants_dir / filename
    if not docx_path.exists():
        pytest.skip(f"нет файла {filename} — пропускаем")
    expected_param, expected_encoding, expected_message = expected

    view = asyncio.run(
        detect_handler(DetectSecretCommand(docx_path=docx_path)),
    )

    assert view.success, view.error
    assert view.method is not None
    assert view.method.param is expected_param
    assert view.encoding is not None
    assert view.encoding.name == expected_encoding
    assert view.message == expected_message


@pytest.mark.parametrize("filename", sorted(KNOWN_FAILURES))
def test_known_failure_variant(
    detect_handler: DetectSecretCommandHandler,
    variants_dir: Path,
    filename: str,
) -> None:
    docx_path = variants_dir / filename
    if not docx_path.exists():
        pytest.skip(f"нет файла {filename} — пропускаем")
    # Документируем известную проблему данных: detect не должен падать,
    # но осмысленного сообщения по этому файлу не извлекается.
    view = asyncio.run(
        detect_handler(DetectSecretCommand(docx_path=docx_path)),
    )
    assert view.docx_path == docx_path
