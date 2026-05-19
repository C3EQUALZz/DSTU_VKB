"""Тесты обучения и оценки модели."""

from __future__ import annotations

import math

import pytest
import torch

from fourth_laboratory.dataset import build_dataset
from fourth_laboratory.model import ShapeClassifier
from fourth_laboratory.train import (
    EvalMetrics,
    TrainConfig,
    evaluate,
    train_model,
)


@pytest.fixture(scope="module")
def small_datasets():
    """Маленький, но достаточный для базовых проверок датасет."""
    return build_dataset(
        n_per_class_train=60, n_per_class_test=15, image_size=20, seed=0
    )


class TestEvaluate:
    def test_metrics_in_valid_range(self, small_datasets) -> None:
        _, test_ds = small_datasets
        model = ShapeClassifier(input_dim=20 * 20, hidden_dim=10)
        metrics = evaluate(model, test_ds)
        assert isinstance(metrics, EvalMetrics)
        assert 0.0 <= metrics.accuracy <= 1.0
        # MSE и MAE на softmax-выходе должны быть конечны и неотрицательны
        assert metrics.mse >= 0.0
        assert metrics.mae >= 0.0
        assert math.isfinite(metrics.mse)
        assert math.isfinite(metrics.mae)


class TestTraining:
    def test_loss_decreases_during_training(self, small_datasets) -> None:
        train_ds, test_ds = small_datasets
        model = ShapeClassifier(input_dim=20 * 20, hidden_dim=32)
        result = train_model(
            model,
            train_ds,
            test_ds,
            TrainConfig(epochs=5, batch_size=32, seed=0),
        )
        assert len(result.train_history) == 5
        # Лосс должен снижаться: последняя эпоха меньше первой
        assert result.train_history[-1] < result.train_history[0]

    def test_accuracy_better_than_chance(self, small_datasets) -> None:
        train_ds, test_ds = small_datasets
        model = ShapeClassifier(input_dim=20 * 20, hidden_dim=64)
        result = train_model(
            model,
            train_ds,
            test_ds,
            TrainConfig(epochs=8, batch_size=32, seed=0),
        )
        assert result.test_metrics is not None
        # Случайная классификация даст ~0.33 на 3 классах.
        # Даже маленькая обученная MLP должна заметно превышать этот уровень.
        assert result.test_metrics.accuracy > 0.5

    def test_num_parameters_recorded(self, small_datasets) -> None:
        train_ds, test_ds = small_datasets
        model = ShapeClassifier(input_dim=20 * 20, hidden_dim=10)
        result = train_model(
            model,
            train_ds,
            test_ds,
            TrainConfig(epochs=1, batch_size=16, seed=0),
        )
        # 20*20*10 + 10 + 10*3 + 3 = 4043
        assert result.num_parameters == 20 * 20 * 10 + 10 + 10 * 3 + 3

    def test_seed_reproducibility(self, small_datasets) -> None:
        train_ds, test_ds = small_datasets

        def run_once() -> float:
            # Засеваем RNG до создания модели, чтобы инициализация
            # весов тоже была воспроизводимой.
            torch.manual_seed(123)
            model = ShapeClassifier(input_dim=20 * 20, hidden_dim=16)
            result = train_model(
                model,
                train_ds,
                test_ds,
                TrainConfig(epochs=3, batch_size=16, seed=123),
            )
            assert result.test_metrics is not None
            return result.test_metrics.accuracy

        a = run_once()
        b = run_once()
        assert a == pytest.approx(b, abs=1e-6)
