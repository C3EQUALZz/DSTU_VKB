"""Тесты подсчёта русских гласных."""

import pytest

from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (
    VowelCounter,
)


@pytest.fixture
def counter() -> VowelCounter:
    return VowelCounter()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Мама мыла раму", 6),
        ("Знание сила", 5),
        ("СТОЛ", 1),
        ("", 0),
        ("ёлка", 2),
        ("xyz123", 0),
    ],
)
def test_counts_russian_vowels(
    counter: VowelCounter, text: str, expected: int,
) -> None:
    assert counter.count(text) == expected
