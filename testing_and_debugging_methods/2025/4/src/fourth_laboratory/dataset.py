"""Программный генератор датасета геометрических фигур.

Генерирует grayscale изображения 28x28 (как MNIST) трёх классов:
    0 — circle (круг)
    1 — square (квадрат)
    2 — triangle (треугольник)

Каждое изображение имеет случайные:
    * размер фигуры (в разумных пределах),
    * положение центра,
    * угол поворота (для треугольников и квадратов),
    * толщину контура (фигура может быть с заливкой или контурной),
    * лёгкий гауссовский шум фона.

Использование:
    >>> from fourth_laboratory.dataset import build_dataset
    >>> X_train, y_train, X_test, y_test = build_dataset(
    ...     n_per_class_train=1000, n_per_class_test=200, image_size=28, seed=42
    ... )
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Literal

import numpy as np
from PIL import Image, ImageDraw

ShapeName = Literal["circle", "square", "triangle"]
SHAPES: tuple[ShapeName, ...] = ("circle", "square", "triangle")
LABEL_OF: dict[ShapeName, int] = {name: idx for idx, name in enumerate(SHAPES)}


# ---------------------------------------------------------------------------
# Внутренние утилиты рисования
# ---------------------------------------------------------------------------

def _random_state(seed: int | None) -> np.random.Generator:
    return np.random.default_rng(seed)


def _draw_circle(
    draw: ImageDraw.ImageDraw,
    image_size: int,
    rng: np.random.Generator,
) -> None:
    radius = rng.integers(low=image_size // 5, high=image_size // 2 - 1)
    cx = rng.integers(low=radius + 1, high=image_size - radius - 1)
    cy = rng.integers(low=radius + 1, high=image_size - radius - 1)
    bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
    filled = bool(rng.integers(0, 2))
    if filled:
        draw.ellipse(bbox, fill=255)
    else:
        outline_width = int(rng.integers(1, 3))
        draw.ellipse(bbox, outline=255, width=outline_width)


def _draw_square(
    draw: ImageDraw.ImageDraw,
    image_size: int,
    rng: np.random.Generator,
) -> None:
    half = int(rng.integers(low=image_size // 5, high=image_size // 2 - 1))
    cx = int(rng.integers(low=half + 1, high=image_size - half - 1))
    cy = int(rng.integers(low=half + 1, high=image_size - half - 1))
    angle = float(rng.uniform(0.0, 90.0))

    # Координаты квадрата с поворотом вокруг (cx, cy)
    corners = [
        (-half, -half),
        (half, -half),
        (half, half),
        (-half, half),
    ]
    cos_a = math.cos(math.radians(angle))
    sin_a = math.sin(math.radians(angle))
    rotated = [
        (cx + cos_a * x - sin_a * y, cy + sin_a * x + cos_a * y)
        for (x, y) in corners
    ]
    filled = bool(rng.integers(0, 2))
    if filled:
        draw.polygon(rotated, fill=255)
    else:
        outline_width = int(rng.integers(1, 3))
        # Рисуем замкнутый контур
        pts = rotated + [rotated[0]]
        draw.line(pts, fill=255, width=outline_width)


def _draw_triangle(
    draw: ImageDraw.ImageDraw,
    image_size: int,
    rng: np.random.Generator,
) -> None:
    # Равносторонний треугольник с поворотом и случайным сдвигом
    radius = int(rng.integers(low=image_size // 4, high=image_size // 2 - 1))
    cx = int(rng.integers(low=radius + 1, high=image_size - radius - 1))
    cy = int(rng.integers(low=radius + 1, high=image_size - radius - 1))
    angle0 = float(rng.uniform(0.0, 120.0))

    pts = []
    for k in range(3):
        theta = math.radians(angle0 + 120.0 * k)
        pts.append((cx + radius * math.cos(theta), cy + radius * math.sin(theta)))
    filled = bool(rng.integers(0, 2))
    if filled:
        draw.polygon(pts, fill=255)
    else:
        outline_width = int(rng.integers(1, 3))
        draw.line(pts + [pts[0]], fill=255, width=outline_width)


_DRAWERS = {
    "circle": _draw_circle,
    "square": _draw_square,
    "triangle": _draw_triangle,
}


# ---------------------------------------------------------------------------
# Открытый API
# ---------------------------------------------------------------------------

def generate_image(
    shape: ShapeName,
    image_size: int = 28,
    rng: np.random.Generator | None = None,
    noise_std: float = 0.03,
) -> np.ndarray:
    """Сгенерировать одно изображение заданной формы.

    Возвращает numpy-массив формы ``(image_size, image_size)`` в float32,
    значения в диапазоне [0.0, 1.0] (с шумом).
    """
    if rng is None:
        rng = np.random.default_rng()
    if shape not in _DRAWERS:
        raise ValueError(f"Unknown shape: {shape!r}. Expected one of {SHAPES}")

    img = Image.new("L", (image_size, image_size), color=0)
    draw = ImageDraw.Draw(img)
    _DRAWERS[shape](draw, image_size, rng)

    arr = np.asarray(img, dtype=np.float32) / 255.0
    if noise_std > 0:
        arr = arr + rng.normal(0.0, noise_std, size=arr.shape).astype(np.float32)
        arr = np.clip(arr, 0.0, 1.0)
    return arr


@dataclass(frozen=True)
class Dataset:
    """Контейнер для пары (X, y) — изображения и целочисленные метки."""

    X: np.ndarray  # shape (N, H, W), dtype float32
    y: np.ndarray  # shape (N,),     dtype int64

    @property
    def n_samples(self) -> int:
        return int(self.X.shape[0])

    @property
    def image_size(self) -> int:
        return int(self.X.shape[1])


def _generate_batch(
    shapes: Iterable[ShapeName],
    n_per_class: int,
    image_size: int,
    rng: np.random.Generator,
    noise_std: float,
) -> Dataset:
    images: list[np.ndarray] = []
    labels: list[int] = []
    for shape in shapes:
        label = LABEL_OF[shape]
        for _ in range(n_per_class):
            images.append(generate_image(shape, image_size, rng, noise_std))
            labels.append(label)
    X = np.stack(images, axis=0).astype(np.float32)
    y = np.asarray(labels, dtype=np.int64)
    # Перемешиваем
    order = rng.permutation(X.shape[0])
    return Dataset(X=X[order], y=y[order])


def build_dataset(
    n_per_class_train: int = 1000,
    n_per_class_test: int = 200,
    image_size: int = 28,
    seed: int | None = 42,
    noise_std: float = 0.03,
) -> tuple[Dataset, Dataset]:
    """Сгенерировать тренировочный и тестовый датасет.

    Параметры:
        n_per_class_train : сколько примеров каждого класса в train
        n_per_class_test  : сколько примеров каждого класса в test
        image_size        : сторона квадратного изображения (по умолчанию 28)
        seed              : seed PRNG; ``None`` даст разный датасет каждый раз
        noise_std         : стандартное отклонение гауссовского шума

    Возвращает: ``(train, test)`` — два объекта ``Dataset``.
    """
    rng = _random_state(seed)
    train = _generate_batch(SHAPES, n_per_class_train, image_size, rng, noise_std)
    test = _generate_batch(SHAPES, n_per_class_test, image_size, rng, noise_std)
    return train, test
