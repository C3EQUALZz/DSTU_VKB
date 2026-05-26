"""Тесты языковой статистики (частоты букв русского)."""

from steganography.domain.text_format_decode.language.russian_language_statistics import (
    RussianLanguageStatistics,
)


def test_known_letter_frequency(
    russian_language: RussianLanguageStatistics,
) -> None:
    assert russian_language.letter_frequency("о") == 0.1097
    assert russian_language.letter_frequency("О") == 0.1097
    assert russian_language.letter_frequency("x") is None


def test_real_text_more_russian_like_than_rare_letters(
    russian_language: RussianLanguageStatistics,
) -> None:
    real = russian_language.likeness("один бог забыл другой поможет")
    rare = russian_language.likeness("щъфэюцщъфэюц")
    assert real > rare


def test_empty_text_returns_neutral(
    russian_language: RussianLanguageStatistics,
) -> None:
    assert russian_language.likeness("") == 1.0
