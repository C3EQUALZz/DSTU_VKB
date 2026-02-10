from typing import final

import torch
from torch import nn

from fulla.domain.shape_recognition.value_objects.activation_type import ActivationType


@final
class ShapeClassifier(nn.Module):
    """Fully-connected neural network with one hidden layer for shape classification."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_classes: int,
        activation: ActivationType,
    ) -> None:
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self._activation: ActivationType = activation

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        if self._activation == ActivationType.RELU:
            x = torch.relu(x)
        return self.fc2(x)

