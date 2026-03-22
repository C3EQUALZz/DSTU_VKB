from dataclasses import dataclass

from text_analyzer.domain.value_objects import ReviewText, Sentiment


@dataclass(frozen=True, slots=True)
class Review:
    text: ReviewText
    sentiment: Sentiment

    @staticmethod
    def create(text: str, sentiment: Sentiment) -> "Review":
        return Review(text=ReviewText(text), sentiment=sentiment)
