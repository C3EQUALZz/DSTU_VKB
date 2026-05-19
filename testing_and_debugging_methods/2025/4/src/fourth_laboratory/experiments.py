"""Перебор гиперпараметров по заданию лабораторной работы №4.

Согласно условию:
    * число нейронов в одном скрытом слое: 10 / 100 / 5000;
    * активация в скрытом слое: relu / linear;
    * batch_size: 10 / 100 / 1000.

Итого 3 × 2 × 3 = 18 экспериментов.
"""

from __future__ import annotations

import itertools
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from fourth_laboratory.dataset import Dataset, build_dataset
from fourth_laboratory.model import Activation, ShapeClassifier
from fourth_laboratory.train import TrainConfig, TrainResult, train_model

HIDDEN_SIZES: tuple[int, ...] = (10, 100, 5000)
ACTIVATIONS: tuple[Activation, ...] = ("relu", "linear")
BATCH_SIZES: tuple[int, ...] = (10, 100, 1000)


@dataclass
class ExperimentConfig:
    hidden_dim: int
    activation: Activation
    batch_size: int


@dataclass
class ExperimentResult:
    config: ExperimentConfig
    accuracy: float
    mse: float
    mae: float
    final_train_loss: float
    num_parameters: int
    elapsed_seconds: float


def all_configs() -> list[ExperimentConfig]:
    """Все 18 экспериментов согласно заданию."""
    return [
        ExperimentConfig(hidden_dim=h, activation=a, batch_size=b)
        for h, a, b in itertools.product(HIDDEN_SIZES, ACTIVATIONS, BATCH_SIZES)
    ]


def run_single_experiment(
    cfg: ExperimentConfig,
    train_ds: Dataset,
    test_ds: Dataset,
    epochs: int = 10,
    learning_rate: float = 1e-3,
    seed: int = 42,
    device: str = "cpu",
) -> ExperimentResult:
    """Один эксперимент с заданной конфигурацией."""
    input_dim = train_ds.image_size * train_ds.image_size
    model = ShapeClassifier(
        input_dim=input_dim,
        hidden_dim=cfg.hidden_dim,
        output_dim=3,
        activation=cfg.activation,
    )
    train_cfg = TrainConfig(
        epochs=epochs,
        batch_size=cfg.batch_size,
        learning_rate=learning_rate,
        seed=seed,
        device=device,
    )

    started = time.perf_counter()
    result: TrainResult = train_model(model, train_ds, test_ds, train_cfg)
    elapsed = time.perf_counter() - started

    assert result.test_metrics is not None
    return ExperimentResult(
        config=cfg,
        accuracy=result.test_metrics.accuracy,
        mse=result.test_metrics.mse,
        mae=result.test_metrics.mae,
        final_train_loss=result.final_train_loss,
        num_parameters=result.num_parameters,
        elapsed_seconds=elapsed,
    )


def run_all(
    configs: Iterable[ExperimentConfig] | None = None,
    n_per_class_train: int = 800,
    n_per_class_test: int = 200,
    image_size: int = 28,
    epochs: int = 10,
    seed: int = 42,
    device: str = "cpu",
    verbose: bool = True,
) -> list[ExperimentResult]:
    """Прогнать все эксперименты на одном фиксированном датасете."""
    train_ds, test_ds = build_dataset(
        n_per_class_train=n_per_class_train,
        n_per_class_test=n_per_class_test,
        image_size=image_size,
        seed=seed,
    )
    if verbose:
        print(
            f"Сгенерирован датасет: train={train_ds.n_samples} | "
            f"test={test_ds.n_samples} | image={train_ds.image_size}x{train_ds.image_size}"
        )

    configs_list = list(configs) if configs is not None else all_configs()
    results: list[ExperimentResult] = []
    for idx, cfg in enumerate(configs_list, start=1):
        if verbose:
            print(
                f"[{idx:>2}/{len(configs_list)}] "
                f"hidden={cfg.hidden_dim:>4d}  act={cfg.activation:<6s}  "
                f"batch={cfg.batch_size:<4d} ...",
                end=" ",
                flush=True,
            )
        res = run_single_experiment(
            cfg, train_ds, test_ds, epochs=epochs, seed=seed, device=device
        )
        results.append(res)
        if verbose:
            print(
                f"acc={res.accuracy:.4f}  mse={res.mse:.4f}  "
                f"mae={res.mae:.4f}  ({res.elapsed_seconds:.1f}s, "
                f"params={res.num_parameters})"
            )
    return results


def format_results_table(results: list[ExperimentResult]) -> str:
    """Markdown-таблица для отчёта."""
    header = (
        "| Hidden | Activation | Batch | Accuracy | MSE    | MAE    | "
        "Final train loss | Params    | Time (s) |\n"
        "|-------:|------------|------:|---------:|-------:|-------:|"
        "-----------------:|----------:|---------:|"
    )
    lines = [header]
    for r in results:
        lines.append(
            f"| {r.config.hidden_dim:>6d} "
            f"| {r.config.activation:<10s} "
            f"| {r.config.batch_size:>5d} "
            f"| {r.accuracy:>8.4f} "
            f"| {r.mse:>6.4f} "
            f"| {r.mae:>6.4f} "
            f"| {r.final_train_loss:>16.4f} "
            f"| {r.num_parameters:>9d} "
            f"| {r.elapsed_seconds:>8.1f} |"
        )
    return "\n".join(lines)


def save_results_json(results: list[ExperimentResult], path: Path) -> None:
    path.write_text(
        json.dumps(
            [
                {
                    "hidden_dim": r.config.hidden_dim,
                    "activation": r.config.activation,
                    "batch_size": r.config.batch_size,
                    "accuracy": r.accuracy,
                    "mse": r.mse,
                    "mae": r.mae,
                    "final_train_loss": r.final_train_loss,
                    "num_parameters": r.num_parameters,
                    "elapsed_seconds": r.elapsed_seconds,
                }
                for r in results
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
