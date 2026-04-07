from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True, slots=True)
class DatasetBundle:
    train_features: npt.NDArray[np.float32]
    train_labels: npt.NDArray[np.int64]
    test_features: npt.NDArray[np.float32]
    test_labels: npt.NDArray[np.int64]
    class_names: tuple[str, ...]
    image_width: int
    image_height: int

    @property
    def input_size(self) -> int:
        return self.image_width * self.image_height


@dataclass(frozen=True, slots=True)
class TrainingConfig:
    data_dir: Path
    artifact_path: Path
    epochs: int = 30
    batch_size: int = 32
    learning_rate: float = 1e-3
    hidden_size: int = 128
    test_size: float = 0.2
    seed: int = 42
    image_width: int = 20
    image_height: int = 20
    device: str = "auto"


@dataclass(frozen=True, slots=True)
class ModelArtifactMetadata:
    class_names: tuple[str, ...]
    image_width: int
    image_height: int
    hidden_size: int

    @property
    def input_size(self) -> int:
        return self.image_width * self.image_height


@dataclass(frozen=True, slots=True)
class TrainingReport:
    artifact_path: Path
    accuracy: float
    device: str
    train_samples: int
    test_samples: int
    class_names: tuple[str, ...]
    epochs: int
    batch_size: int
    learning_rate: float
    hidden_size: int
    loss_history: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class PredictionResult:
    label: str
    confidence: float
    probabilities: dict[str, float]


@dataclass(frozen=True, slots=True)
class PredictionHistoryEntry:
    id: int
    filename: str | None
    content_type: str | None
    file_size_bytes: int
    label: str
    confidence: float
    probabilities: dict[str, float]
    created_at: datetime
