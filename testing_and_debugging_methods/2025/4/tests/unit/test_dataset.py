"""Тесты генератора датасета."""

from __future__ import annotations

import numpy as np
import pytest

from fourth_laboratory.dataset import (
    LABEL_OF,
    SHAPES,
    Dataset,
    build_dataset,
    generate_image,
)


class TestGenerateImage:
    @pytest.mark.parametrize("shape", SHAPES)
    def test_shape_and_dtype(self, shape: str) -> None:
        img = generate_image(shape, image_size=28)
        assert img.shape == (28, 28)
        assert img.dtype == np.float32

    @pytest.mark.parametrize("shape", SHAPES)
    def test_values_in_unit_range(self, shape: str) -> None:
        img = generate_image(shape, image_size=32)
        assert float(img.min()) >= 0.0
        assert float(img.max()) <= 1.0

    @pytest.mark.parametrize("shape", SHAPES)
    def test_image_is_not_empty(self, shape: str) -> None:
        # Хотя бы какие-то пиксели "светлые" — фигура нарисована.
        rng = np.random.default_rng(0)
        img = generate_image(shape, image_size=28, rng=rng, noise_std=0.0)
        assert (img > 0.5).sum() > 5, "Изображение фигуры пустое"

    def test_unknown_shape_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown shape"):
            generate_image("pentagon", image_size=28)  # type: ignore[arg-type]

    def test_deterministic_with_seed(self) -> None:
        rng1 = np.random.default_rng(123)
        rng2 = np.random.default_rng(123)
        img1 = generate_image("circle", image_size=28, rng=rng1, noise_std=0.0)
        img2 = generate_image("circle", image_size=28, rng=rng2, noise_std=0.0)
        assert np.array_equal(img1, img2)


class TestBuildDataset:
    def test_shapes(self) -> None:
        train, test = build_dataset(
            n_per_class_train=10, n_per_class_test=4, image_size=20, seed=7
        )
        assert isinstance(train, Dataset)
        assert isinstance(test, Dataset)
        # 3 класса × 10 = 30 train, 3 × 4 = 12 test
        assert train.X.shape == (30, 20, 20)
        assert train.y.shape == (30,)
        assert test.X.shape == (12, 20, 20)
        assert test.y.shape == (12,)

    def test_dtypes(self) -> None:
        train, test = build_dataset(n_per_class_train=5, n_per_class_test=5, seed=0)
        assert train.X.dtype == np.float32
        assert train.y.dtype == np.int64
        assert test.X.dtype == np.float32
        assert test.y.dtype == np.int64

    def test_label_set_covers_all_classes(self) -> None:
        train, test = build_dataset(n_per_class_train=20, n_per_class_test=10, seed=0)
        assert set(train.y.tolist()) == set(LABEL_OF.values())
        assert set(test.y.tolist()) == set(LABEL_OF.values())

    def test_balanced_train(self) -> None:
        train, _ = build_dataset(n_per_class_train=30, n_per_class_test=5, seed=0)
        counts = np.bincount(train.y, minlength=3)
        # каждый класс встречается одинаковое число раз
        assert counts.tolist() == [30, 30, 30]

    def test_deterministic_with_same_seed(self) -> None:
        a_train, a_test = build_dataset(n_per_class_train=10, n_per_class_test=5, seed=42)
        b_train, b_test = build_dataset(n_per_class_train=10, n_per_class_test=5, seed=42)
        assert np.array_equal(a_train.X, b_train.X)
        assert np.array_equal(a_train.y, b_train.y)
        assert np.array_equal(a_test.X, b_test.X)
        assert np.array_equal(a_test.y, b_test.y)
