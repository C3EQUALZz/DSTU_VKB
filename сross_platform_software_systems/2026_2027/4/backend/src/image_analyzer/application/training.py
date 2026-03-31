import json
from dataclasses import asdict

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from image_analyzer.domain.types import ModelArtifactMetadata, TrainingConfig, TrainingReport
from image_analyzer.infrastructure.dataset import ShapeDatasetLoader
from image_analyzer.infrastructure.model import ShapeClassifier, save_artifact


def resolve_device(device_name: str) -> torch.device:
    if device_name != "auto":
        return torch.device(device_name)
    if torch.cuda.is_available():
        return torch.device("cuda")
    mps_backend = getattr(torch.backends, "mps", None)
    if mps_backend is not None and mps_backend.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def train_and_save_model(config: TrainingConfig) -> TrainingReport:
    dataset = ShapeDatasetLoader(
        data_dir=config.data_dir,
        image_width=config.image_width,
        image_height=config.image_height,
        test_size=config.test_size,
        seed=config.seed,
    ).load()

    device = resolve_device(config.device)
    train_loader = DataLoader(
        TensorDataset(
            torch.tensor(dataset.train_features, dtype=torch.float32),
            torch.tensor(dataset.train_labels, dtype=torch.long),
        ),
        batch_size=config.batch_size,
        shuffle=True,
    )
    test_loader = DataLoader(
        TensorDataset(
            torch.tensor(dataset.test_features, dtype=torch.float32),
            torch.tensor(dataset.test_labels, dtype=torch.long),
        ),
        batch_size=config.batch_size,
        shuffle=False,
    )

    model = ShapeClassifier(
        input_size=dataset.input_size,
        hidden_size=config.hidden_size,
        num_classes=len(dataset.class_names),
    ).to(device)
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()
    loss_history = _train_loop(
        model=model,
        loader=train_loader,
        optimizer=optimizer,
        criterion=criterion,
        epochs=config.epochs,
        device=device,
    )
    accuracy = _evaluate(model=model, loader=test_loader, device=device)

    metadata = ModelArtifactMetadata(
        class_names=dataset.class_names,
        image_width=dataset.image_width,
        image_height=dataset.image_height,
        hidden_size=config.hidden_size,
    )
    save_artifact(model, metadata, config.artifact_path)

    report = TrainingReport(
        artifact_path=config.artifact_path,
        accuracy=accuracy,
        device=device.type,
        train_samples=int(dataset.train_features.shape[0]),
        test_samples=int(dataset.test_features.shape[0]),
        class_names=dataset.class_names,
        epochs=config.epochs,
        batch_size=config.batch_size,
        learning_rate=config.learning_rate,
        hidden_size=config.hidden_size,
        loss_history=tuple(loss_history),
    )
    _write_training_report(report)
    return report


def _train_loop(
    model: ShapeClassifier,
    loader: DataLoader,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    epochs: int,
    device: torch.device,
) -> list[float]:
    model.train()
    history: list[float] = []

    for _ in range(epochs):
        total_loss = 0.0
        total_samples = 0

        for features, labels in loader:
            batch_features = features.to(device)
            batch_labels = labels.to(device)

            optimizer.zero_grad()
            logits = model(batch_features)
            loss = criterion(logits, batch_labels)
            loss.backward()
            optimizer.step()

            total_loss += float(loss.item()) * batch_features.size(0)
            total_samples += int(batch_features.size(0))

        history.append(total_loss / total_samples)

    return history


@torch.no_grad()
def _evaluate(model: ShapeClassifier, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    correct = 0
    total = 0

    for features, labels in loader:
        batch_features = features.to(device)
        batch_labels = labels.to(device)
        predictions = model(batch_features).argmax(dim=1)
        total += int(batch_labels.size(0))
        correct += int((predictions == batch_labels).sum().item())

    return correct / total if total else 0.0


def _write_training_report(report: TrainingReport) -> None:
    report_path = report.artifact_path.with_suffix(".json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    serializable_report = asdict(report)
    serializable_report["artifact_path"] = str(report.artifact_path)
    with report_path.open("w", encoding="utf-8") as file:
        json.dump(serializable_report, file, ensure_ascii=True, indent=2)
