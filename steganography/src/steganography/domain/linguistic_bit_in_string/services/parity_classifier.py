"""ParityClassifier — относит строку к Y- или N-подмножеству.

Метод: чётность числа русских гласных. Строки с чётным количеством
гласных входят в Y-множество (бит «1», ответ «ДА»), с нечётным —
в N-множество (бит «0», ответ «НЕТ»).
"""

from typing import Final, final

from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (
    VowelCounter,
)
from steganography.domain.linguistic_bit_in_string.value_objects.string_classification import (
    StringClassification,
)

_ANSWER_YES: Final[str] = "ДА"
_ANSWER_NO: Final[str] = "НЕТ"


@final
class ParityClassifier:
    """Доменный сервис классификации строки по чётности числа гласных."""

    def __init__(self, vowel_counter: VowelCounter) -> None:
        self._vowel_counter = vowel_counter

    def classify(self, text: str) -> StringClassification:
        vowels = self._vowel_counter.count(text)
        is_even = vowels % 2 == 0
        return StringClassification(
            text=text,
            bit=1 if is_even else 0,
            answer=_ANSWER_YES if is_even else _ANSWER_NO,
            feature_value=vowels,
        )
