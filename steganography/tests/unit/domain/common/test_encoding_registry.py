"""Тесты реестра кодировок."""

from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)


def test_registry_exposes_all_five_encodings(
    encoding_registry: EncodingRegistry,
) -> None:
    names = {enc.name for enc in encoding_registry.all()}
    assert names == {
        "МТК-2 (Бодо)",
        "КОИ-8R",
        "cp866",
        "Windows-1251",
        "ASCII",
    }


def test_mtk2_property_matches_registry(
    encoding_registry: EncodingRegistry,
) -> None:
    assert encoding_registry.mtk2 in encoding_registry.all()
    assert encoding_registry.mtk2.name == "МТК-2 (Бодо)"
