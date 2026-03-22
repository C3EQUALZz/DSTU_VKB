import json
import logging
import re
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Final, final

logger: Final[logging.Logger] = logging.getLogger(__name__)

_PAD_TOKEN: Final[str] = "<PAD>"
_UNK_TOKEN: Final[str] = "<UNK>"
_PAD_IDX: Final[int] = 0
_UNK_IDX: Final[int] = 1

_WORD_PATTERN: Final[re.Pattern[str]] = re.compile(r"[а-яёa-z0-9]+", re.IGNORECASE)
_CHAR_NGRAM_MIN: Final[int] = 2
_CHAR_NGRAM_MAX: Final[int] = 5


@final
class SimpleTextPreprocessor:
    def __init__(self) -> None:
        self._vocab: dict[str, int] = {}
        self._vocab_built: bool = False

    def fit(self, texts: Sequence[str], max_vocab_size: int) -> None:
        counter: Counter[str] = Counter()
        for text in texts:
            tokens = self._tokenize(text)
            counter.update(tokens)

        self._vocab = {_PAD_TOKEN: _PAD_IDX, _UNK_TOKEN: _UNK_IDX}
        for token, _ in counter.most_common(max_vocab_size - 2):
            self._vocab[token] = len(self._vocab)

        self._vocab_built = True
        logger.info("Vocabulary built: %d tokens (from %d unique)", len(self._vocab), len(counter))

    def encode(self, texts: Sequence[str], max_length: int) -> list[list[int]]:
        if not self._vocab_built:
            msg = "Vocabulary not built. Call fit() first."
            raise RuntimeError(msg)

        encoded: list[list[int]] = []
        for text in texts:
            tokens = self._tokenize(text)
            indices = [self._vocab.get(t, _UNK_IDX) for t in tokens]

            if len(indices) < max_length:
                indices.extend([_PAD_IDX] * (max_length - len(indices)))
            else:
                indices = indices[:max_length]

            encoded.append(indices)

        return encoded

    @property
    def vocab_size(self) -> int:
        return len(self._vocab)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self._vocab, ensure_ascii=False), encoding="utf-8")
        logger.info("Vocabulary saved to %s", path)

    def load(self, path: Path) -> None:
        self._vocab = json.loads(path.read_text(encoding="utf-8"))
        self._vocab_built = True
        logger.info("Vocabulary loaded from %s (%d tokens)", path, len(self._vocab))

    @classmethod
    def _tokenize(cls, text: str) -> list[str]:
        lower = text.lower()
        words = _WORD_PATTERN.findall(lower)
        tokens: list[str] = list(words)

        for i in range(len(words) - 1):
            tokens.append(f"w_{words[i]}_{words[i + 1]}")

        for word in words:
            padded = f" {word} "
            for n in range(_CHAR_NGRAM_MIN, _CHAR_NGRAM_MAX + 1):
                for start in range(len(padded) - n + 1):
                    tokens.append(f"c_{padded[start:start + n]}")

        return tokens
