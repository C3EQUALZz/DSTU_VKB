class DomainError(Exception):
    pass


class EmptyReviewTextError(DomainError):
    def __init__(self) -> None:
        super().__init__("Review text cannot be empty")


class InvalidSentimentError(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid sentiment value: {value}")
