from collections.abc import Sequence
from pathlib import Path
from typing import Protocol


class TextPreprocessor(Protocol):
    def fit(self, texts: Sequence[str], max_vocab_size: int) -> None:
        """Build vocabulary from training texts."""
        ...

    def encode(self, texts: Sequence[str], max_length: int) -> list[list[int]]:
        """Encode texts as sequences of token indices."""
        ...

    @property
    def vocab_size(self) -> int:
        """Return the size of the vocabulary (including special tokens)."""
        ...

    def save(self, path: Path) -> None:
        """Save vocabulary to file."""
        ...

    def load(self, path: Path) -> None:
        """Load vocabulary from file."""
        ...
