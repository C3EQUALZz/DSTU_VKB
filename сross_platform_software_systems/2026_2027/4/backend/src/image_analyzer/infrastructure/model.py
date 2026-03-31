from dataclasses import asdict
from pathlib import Path

import torch
from torch import nn

from image_analyzer.domain.types import ModelArtifactMetadata


class ShapeClassifier(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, num_classes: int) -> None:
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        hidden = torch.relu(self.fc1(inputs))
        return self.fc2(hidden)


def save_artifact(model: ShapeClassifier, metadata: ModelArtifactMetadata, artifact_path: Path) -> None:
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "metadata": asdict(metadata),
        },
        artifact_path,
    )


def load_artifact(artifact_path: Path, device: torch.device) -> tuple[ShapeClassifier, ModelArtifactMetadata]:
    payload = torch.load(artifact_path, map_location=device)
    metadata_raw = payload["metadata"]
    metadata = ModelArtifactMetadata(
        class_names=tuple(metadata_raw["class_names"]),
        image_width=int(metadata_raw["image_width"]),
        image_height=int(metadata_raw["image_height"]),
        hidden_size=int(metadata_raw["hidden_size"]),
    )

    model = ShapeClassifier(
        input_size=metadata.input_size,
        hidden_size=metadata.hidden_size,
        num_classes=len(metadata.class_names),
    ).to(device)
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return model, metadata
