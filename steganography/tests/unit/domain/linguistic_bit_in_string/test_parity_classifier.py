"""Тесты классификации по чётности гласных и длине первого слова."""

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
    # «Верёвочка» — 4 гласных; первое слово содержит 9 букв.
    result = classifier.classify("Верёвочка")
    assert result.bit == 1
    assert result.answer == "ДА"
    assert result.feature_value == 4
    assert result.first_word_length == 9


def test_odd_vowels_yield_no(classifier: ParityClassifier) -> None:
    # «Знание сила» — 5 гласных (нечётное)
    result = classifier.classify("Знание сила")
    assert result.bit == 0
    assert result.answer == "НЕТ"
    assert result.feature_value == 5
    assert result.first_word_length == 6


@pytest.mark.parametrize("text", ["", "xyz", "123"])
def test_text_without_a_long_first_word_yields_no(
    classifier: ParityClassifier, text: str,
) -> None:
    result = classifier.classify(text)
    assert result.bit == 0
    assert result.answer == "НЕТ"


def test_even_vowels_with_short_first_word_yield_no(
    classifier: ParityClassifier,
) -> None:
    result = classifier.classify("Весна, весна на улице,")
    assert result.feature_value == 8
    assert result.first_word_length == 5
    assert result.answer == "НЕТ"


def test_first_word_ignores_punctuation_and_counts_hyphenated_letters(
    classifier: ParityClassifier,
) -> None:
    result = classifier.classify("«Когда-нибудь» всё получится")
    assert result.first_word_length == 11
