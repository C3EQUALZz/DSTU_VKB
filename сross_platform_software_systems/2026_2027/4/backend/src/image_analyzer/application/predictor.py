import numpy as np
import torch

from image_analyzer.application.training import resolve_device
from image_analyzer.domain.types import PredictionResult
from image_analyzer.infrastructure.dataset import preprocess_image_bytes
from image_analyzer.infrastructure.model import ShapeClassifier, load_artifact


class ShapePredictor:
    def __init__(
        self,
        model: ShapeClassifier,
        class_names: tuple[str, ...],
        image_width: int,
        image_height: int,
        device: torch.device,
    ) -> None:
        self._model = model
        self._class_names = class_names
        self._image_width = image_width
        self._image_height = image_height
        self._device = device

    @classmethod
    def from_artifact(cls, artifact_path, device_name: str = "auto") -> "ShapePredictor":
        device = resolve_device(device_name)
        model, metadata = load_artifact(artifact_path=artifact_path, device=device)
        return cls(
            model=model,
            class_names=metadata.class_names,
            image_width=metadata.image_width,
            image_height=metadata.image_height,
            device=device,
        )

    @torch.no_grad()
    def predict(self, image_bytes: bytes) -> PredictionResult:
        feature_vector = preprocess_image_bytes(
            image_bytes=image_bytes,
            image_width=self._image_width,
            image_height=self._image_height,
        )
        tensor = torch.tensor(feature_vector, dtype=torch.float32, device=self._device).unsqueeze(0)
        logits = self._model(tensor)
        probabilities_tensor = torch.softmax(logits, dim=1).squeeze(0).cpu()
        probabilities = probabilities_tensor.numpy().astype(np.float64)

        best_index = int(probabilities.argmax())
        return PredictionResult(
            label=self._class_names[best_index],
            confidence=float(probabilities[best_index]),
            probabilities={
                class_name: float(probability)
                for class_name, probability in zip(self._class_names, probabilities, strict=True)
            },
        )
