"""Цикл обучения и оценки модели.

Метрики оценки:
    * accuracy  — доля верно предсказанных меток;
    * mse, mae  — на one-hot целевом векторе против softmax(logits);
                  такая постановка соответствует заданию (MSE / MAE на
                  тестовой выборке).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from fourth_laboratory.dataset import Dataset


@dataclass
class TrainConfig:
    epochs: int = 10
    batch_size: int = 100
    learning_rate: float = 1e-3
    seed: int | None = 42
    device: str = "cpu"


@dataclass
class EvalMetrics:
    accuracy: float
    mse: float
    mae: float


@dataclass
class TrainResult:
    train_history: list[float] = field(default_factory=list)
    final_train_loss: float = float("nan")
    test_metrics: EvalMetrics | None = None
    num_parameters: int = 0


def _to_tensor_dataset(ds: Dataset) -> TensorDataset:
    X = torch.from_numpy(ds.X)            # (N, H, W) float32
    y = torch.from_numpy(ds.y).long()     # (N,) int64
    return TensorDataset(X, y)


def _seed_everything(seed: int | None) -> None:
    if seed is None:
        return
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def evaluate(
    model: nn.Module,
    test_ds: Dataset,
    device: str = "cpu",
    batch_size: int = 256,
) -> EvalMetrics:
    """Прогнать модель на тестовой выборке и вернуть accuracy/MSE/MAE."""
    model.eval()
    loader = DataLoader(_to_tensor_dataset(test_ds), batch_size=batch_size)
    n_classes = int(model.fc2.out_features) if hasattr(model, "fc2") else 3

    correct = 0
    total = 0
    sq_err_sum = 0.0
    abs_err_sum = 0.0
    elements = 0

    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            logits = model(xb)
            probs = F.softmax(logits, dim=1)
            preds = torch.argmax(logits, dim=1)
            correct += int((preds == yb).sum().item())
            total += yb.size(0)

            one_hot = F.one_hot(yb, num_classes=n_classes).float()
            diff = probs - one_hot
            sq_err_sum += float((diff * diff).sum().item())
            abs_err_sum += float(diff.abs().sum().item())
            elements += diff.numel()

    accuracy = correct / total if total else float("nan")
    mse = sq_err_sum / elements if elements else float("nan")
    mae = abs_err_sum / elements if elements else float("nan")
    return EvalMetrics(accuracy=accuracy, mse=mse, mae=mae)


def train_model(
    model: nn.Module,
    train_ds: Dataset,
    test_ds: Dataset | None = None,
    config: TrainConfig | None = None,
) -> TrainResult:
    """Обучить модель и (опционально) оценить на тесте."""
    cfg = config or TrainConfig()
    _seed_everything(cfg.seed)

    device = torch.device(cfg.device)
    model = model.to(device)

    # Детерминированный shuffle: при наличии seed используем
    # фиксированный torch.Generator, иначе DataLoader заведёт свой.
    if cfg.seed is not None:
        loader_generator = torch.Generator()
        loader_generator.manual_seed(cfg.seed)
    else:
        loader_generator = None
    loader = DataLoader(
        _to_tensor_dataset(train_ds),
        batch_size=cfg.batch_size,
        shuffle=True,
        drop_last=False,
        generator=loader_generator,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    criterion = nn.CrossEntropyLoss()

    history: list[float] = []
    for epoch in range(cfg.epochs):
        model.train()
        running = 0.0
        n_batches = 0
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()
            running += float(loss.item())
            n_batches += 1
        epoch_loss = running / max(n_batches, 1)
        history.append(epoch_loss)

    result = TrainResult(
        train_history=history,
        final_train_loss=history[-1] if history else float("nan"),
        num_parameters=sum(
            p.numel() for p in model.parameters() if p.requires_grad
        ),
    )
    if test_ds is not None:
        result.test_metrics = evaluate(model, test_ds, device=cfg.device)
    return result
