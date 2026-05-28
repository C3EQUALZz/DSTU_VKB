"""Тесты ParityClassifier — отнесение строки к Y или N по чётности гласных."""

import pytest

from steganography.domain.linguistic_bit_in_string.services.parity_classifier import (
    ParityClassifier,
)
from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (
    VowelCounter,
)


@pytest.fixture
def classifier() -> ParityClassifier:
    return ParityClassifier(vowel_counter=VowelCounter())


def test_even_vowels_yield_yes(classifier: ParityClassifier) -> None:
    # «Мама мыла раму» — 6 гласных (чётное)
    result = classifier.classify("Мама мыла раму")
    assert result.bit == 1
    assert result.answer == "ДА"
    assert result.feature_value == 6


def test_odd_vowels_yield_no(classifier: ParityClassifier) -> None:
    # «Знание сила» — 5 гласных (нечётное)
    result = classifier.classify("Знание сила")
    assert result.bit == 0
    assert result.answer == "НЕТ"
    assert result.feature_value == 5


@pytest.mark.parametrize("text", ["", "xyz", "123"])
def test_strings_without_vowels_are_yes(
    classifier: ParityClassifier, text: str,
) -> None:
    # 0 гласных — чётное → ДА
    result = classifier.classify(text)
    assert result.bit == 1
    assert result.answer == "ДА"
