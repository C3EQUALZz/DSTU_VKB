from dataclasses import dataclass
from enum import StrEnum

from text_analyzer.domain.errors import EmptyReviewTextError


class Sentiment(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

    def to_label(self) -> int:
        return 1 if self == Sentiment.POSITIVE else 0

    @staticmethod
    def from_label(label: int) -> "Sentiment":
        return Sentiment.POSITIVE if label == 1 else Sentiment.NEGATIVE


@dataclass(frozen=True, eq=True, slots=True)
class ReviewText:
    value: str

    def __post_init__(self) -> None:
        stripped = self.value.strip()
        if not stripped:
            raise EmptyReviewTextError
        object.__setattr__(self, "value", stripped)

    def __str__(self) -> str:
        return self.value
