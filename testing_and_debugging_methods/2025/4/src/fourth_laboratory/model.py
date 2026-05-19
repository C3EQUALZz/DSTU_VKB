"""Полносвязная (Fully-Connected / MLP) архитектура на PyTorch.

Параметры:
    * ``input_dim``  — размер плоского входа (H*W);
    * ``hidden_dim`` — число нейронов в скрытом слое (10 / 100 / 5000 по заданию);
    * ``output_dim`` — число классов (3 — круг/квадрат/треугольник);
    * ``activation`` — ``"relu"`` или ``"linear"``.

Архитектура:
    Flatten → Linear(input_dim, hidden_dim) → Activation → Linear(hidden_dim, output_dim)

Выход — логиты (без softmax). Применять softmax/argmax уже на стороне
оценки или внутри ``CrossEntropyLoss``.
"""

from __future__ import annotations

from typing import Literal

import torch
import torch.nn as nn

Activation = Literal["relu", "linear"]


def _make_activation(name: Activation) -> nn.Module:
    if name == "relu":
        return nn.ReLU()
    if name == "linear":
        # "Linear" в смысле задания — отсутствие нелинейности.
        return nn.Identity()
    raise ValueError(
        f"Unknown activation: {name!r}. Expected one of {('relu', 'linear')}"
    )


class ShapeClassifier(nn.Module):
    """Полносвязная сеть с одним скрытым слоем для классификации фигур."""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int = 3,
        activation: Activation = "relu",
    ) -> None:
        super().__init__()
        if input_dim <= 0:
            raise ValueError(f"input_dim must be positive, got {input_dim}")
        if hidden_dim <= 0:
            raise ValueError(f"hidden_dim must be positive, got {hidden_dim}")
        if output_dim <= 0:
            raise ValueError(f"output_dim must be positive, got {output_dim}")

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.activation_name = activation

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.act = _make_activation(activation)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x ожидается формы (B, H, W) либо (B, input_dim)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.act(x)
        return self.fc2(x)

    def num_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
