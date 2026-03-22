import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final, final

from text_analyzer.application.dto import TrainingConfig
from text_analyzer.application.ports.classifier import SentimentClassifier
from text_analyzer.application.ports.text_preprocessor import TextPreprocessor
from text_analyzer.domain.value_objects import Sentiment

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class PredictCommand:
    text: str
    model_dir: Path
    config: TrainingConfig


@dataclass(frozen=True, slots=True)
class PredictResult:
    sentiment: Sentiment
    text: str


@final
class PredictCommandHandler:
    def __init__(
        self,
        text_preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
    ) -> None:
        self._text_preprocessor: Final[TextPreprocessor] = text_preprocessor
        self._classifier: Final[SentimentClassifier] = classifier

    def __call__(self, data: PredictCommand) -> PredictResult:
        vocab_path = data.model_dir / "vocab.json"
        model_path = data.model_dir / "model.pt"

        logger.info("Loading vocabulary from %s", vocab_path)
        self._text_preprocessor.load(vocab_path)

        logger.info("Loading model from %s", model_path)
        self._classifier.load_model(
            model_path,
            vocab_size=self._text_preprocessor.vocab_size,
            config=data.config,
        )

        encoded = self._text_preprocessor.encode([data.text], data.config.max_seq_length)
        labels = self._classifier.predict(encoded)
        sentiment = Sentiment.from_label(labels[0])

        logger.info("Prediction: %s", sentiment.value)
        return PredictResult(sentiment=sentiment, text=data.text)
