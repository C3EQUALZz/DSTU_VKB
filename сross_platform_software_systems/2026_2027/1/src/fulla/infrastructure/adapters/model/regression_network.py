from typing import final

import torch
from torch import nn

from fulla.domain.price_prediction.value_objects.regression_activation_type import RegressionActivationType


def _make_activation(activation: RegressionActivationType) -> nn.Module:
    """Create a PyTorch activation module from the domain enum."""
    if activation == RegressionActivationType.RELU:
        return nn.ReLU()
    if activation == RegressionActivationType.TANH:
        return nn.Tanh()
    if activation == RegressionActivationType.LEAKY_RELU:
        return nn.LeakyReLU()
    msg = f"Unsupported activation: {activation}"
    raise ValueError(msg)


@final
class RegressionNetwork(nn.Module):
    """Fully-connected neural network for regression with configurable depth and width."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_hidden_layers: int,
        activation: RegressionActivationType,
    ) -> None:
        super().__init__()

        layers: list[nn.Module] = []

        # First hidden layer
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(_make_activation(activation))

        # Additional hidden layers
        for _ in range(num_hidden_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(_make_activation(activation))

        # Output layer (single value for regression)
        layers.append(nn.Linear(hidden_size, 1))

        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x).squeeze(-1)


