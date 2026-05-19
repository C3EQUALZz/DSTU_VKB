"""CLI entry-point: запуск всех экспериментов.

Использование::

    uv run python -m fourth_laboratory
    uv run python -m fourth_laboratory --epochs 5
    uv run python -m fourth_laboratory --output results.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from fourth_laboratory.experiments import (
    format_results_table,
    run_all,
    save_results_json,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fourth_laboratory",
        description="Перебор гиперпараметров MLP для классификации фигур",
    )
    parser.add_argument("--epochs", type=int, default=10, help="число эпох (default: 10)")
    parser.add_argument("--seed", type=int, default=42, help="seed PRNG (default: 42)")
    parser.add_argument(
        "--n-train",
        type=int,
        default=800,
        help="изображений каждого класса в train (default: 800)",
    )
    parser.add_argument(
        "--n-test",
        type=int,
        default=200,
        help="изображений каждого класса в test (default: 200)",
    )
    parser.add_argument(
        "--image-size", type=int, default=28, help="сторона картинки (default: 28)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=("auto", "cpu", "cuda", "mps"),
        help="устройство torch (default: auto)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="путь к JSON-файлу для сохранения результатов",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="не печатать ход экспериментов, только итоговую таблицу",
    )
    return parser.parse_args()


def _pick_device(name: str) -> str:
    if name != "auto":
        return name
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main() -> None:
    args = _parse_args()
    device = _pick_device(args.device)
    print(f"Устройство: {device}")
    print(f"Эпох: {args.epochs}, seed: {args.seed}")
    print()

    results = run_all(
        n_per_class_train=args.n_train,
        n_per_class_test=args.n_test,
        image_size=args.image_size,
        epochs=args.epochs,
        seed=args.seed,
        device=device,
        verbose=not args.quiet,
    )

    print()
    print("Итоговая таблица результатов:")
    print()
    print(format_results_table(results))

    if args.output is not None:
        save_results_json(results, args.output)
        print(f"\nРезультаты сохранены: {args.output}")


if __name__ == "__main__":
    main()
