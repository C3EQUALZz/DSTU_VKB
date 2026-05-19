"""Тесты MLP-модели."""

from __future__ import annotations

import pytest
import torch

from fourth_laboratory.model import ShapeClassifier


class TestModelConstruction:
    @pytest.mark.parametrize("hidden", [10, 100, 5000])
    @pytest.mark.parametrize("activation", ["relu", "linear"])
    def test_construct_all_lab_configs(
        self, hidden: int, activation: str
    ) -> None:
        # Любая комбинация из задания должна успешно конструироваться.
        model = ShapeClassifier(
            input_dim=28 * 28, hidden_dim=hidden, activation=activation
        )
        assert isinstance(model, torch.nn.Module)

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"input_dim": 0, "hidden_dim": 10},
            {"input_dim": -1, "hidden_dim": 10},
            {"input_dim": 784, "hidden_dim": 0},
            {"input_dim": 784, "hidden_dim": -3},
            {"input_dim": 784, "hidden_dim": 10, "output_dim": 0},
        ],
    )
    def test_invalid_dimensions_raise(self, kwargs: dict) -> None:
        with pytest.raises(ValueError):
            ShapeClassifier(**kwargs)

    def test_invalid_activation_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown activation"):
            ShapeClassifier(input_dim=784, hidden_dim=10, activation="tanh")  # type: ignore[arg-type]


class TestForwardPass:
    def test_output_shape_from_3d_input(self) -> None:
        model = ShapeClassifier(input_dim=28 * 28, hidden_dim=64)
        x = torch.randn(8, 28, 28)
        out = model(x)
        assert out.shape == (8, 3)

    def test_output_shape_from_flat_input(self) -> None:
        model = ShapeClassifier(input_dim=28 * 28, hidden_dim=64)
        x = torch.randn(4, 28 * 28)
        out = model(x)
        assert out.shape == (4, 3)

    def test_linear_activation_is_identity(self) -> None:
        # Если активация linear, проверим что nn.Identity на месте.
        model = ShapeClassifier(input_dim=10, hidden_dim=4, activation="linear")
        assert isinstance(model.act, torch.nn.Identity)

    def test_relu_activation_is_relu(self) -> None:
        model = ShapeClassifier(input_dim=10, hidden_dim=4, activation="relu")
        assert isinstance(model.act, torch.nn.ReLU)


class TestParameterCount:
    @pytest.mark.parametrize(
        ("hidden", "expected_params"),
        [
            # fc1: 784*h + h  |  fc2: h*3 + 3
            (10,   784 * 10 + 10 + 10 * 3 + 3),
            (100,  784 * 100 + 100 + 100 * 3 + 3),
            (5000, 784 * 5000 + 5000 + 5000 * 3 + 3),
        ],
    )
    def test_parameter_count_matches_formula(
        self, hidden: int, expected_params: int
    ) -> None:
        model = ShapeClassifier(input_dim=784, hidden_dim=hidden)
        assert model.num_parameters() == expected_params
