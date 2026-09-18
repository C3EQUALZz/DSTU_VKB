"""ParityClassifier — относит строку к Y- или N-подмножеству.

В Y-множество входят строки с чётным количеством русских гласных,
у которых первое слово содержит больше пяти букв. Остальные строки
входят в N-множество.
"""

import re
from typing import Final, final

from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (
    VowelCounter,
)
from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)

_ANSWER_YES: Final[str] = "ДА"
_ANSWER_NO: Final[str] = "НЕТ"
_MIN_FIRST_WORD_LENGTH: Final[int] = 5
_FIRST_WORD_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"[^\W\d_]+(?:-[^\W\d_]+)*",
)


@final
class ParityClassifier:
    """Классифицирует строку по чётности гласных и длине первого слова."""

    def __init__(self, vowel_counter: VowelCounter) -> None:
        self._vowel_counter = vowel_counter

    def classify(self, text: str) -> StringClassification:
        vowels = self._vowel_counter.count(text)
        first_word_match = _FIRST_WORD_PATTERN.search(text)
        first_word_length = (
            sum(character.isalpha() for character in first_word_match.group())
            if first_word_match is not None
            else 0
        )
        belongs_to_y = (
            vowels % 2 == 0
            and first_word_length > _MIN_FIRST_WORD_LENGTH
        )
        return StringClassification(
            text=text,
            bit=1 if belongs_to_y else 0,
            answer=_ANSWER_YES if belongs_to_y else _ANSWER_NO,
            feature_value=vowels,
            first_word_length=first_word_length,
        )
