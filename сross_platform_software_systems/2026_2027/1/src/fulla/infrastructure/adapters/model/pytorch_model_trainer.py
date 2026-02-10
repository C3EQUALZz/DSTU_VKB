import logging
from typing import Final, final

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset
from fulla.domain.shape_recognition.value_objects.experiment_result import ExperimentResult
from fulla.domain.shape_recognition.value_objects.hyper_parameters import HyperParameters
from fulla.infrastructure.adapters.model.shape_classifier import ShapeClassifier

logger: Final[logging.Logger] = logging.getLogger(__name__)

CLASS_COUNT: Final[int] = 3


@final
class PyTorchModelTrainer:
    """Trains a ShapeClassifier and evaluates it using PyTorch."""

    def __init__(
        self,
        epochs: int,
        learning_rate: float,
        device: torch.device,
    ) -> None:
        self._epochs: Final[int] = epochs
        self._learning_rate: Final[float] = learning_rate
        self._device: Final[torch.device] = device

    def train_and_evaluate(
        self,
        dataset: PreparedDataset,
        params: HyperParameters,
    ) -> ExperimentResult:
        x_train = torch.tensor(dataset.x_train, dtype=torch.float32)
        y_train = torch.tensor(dataset.y_train, dtype=torch.long)
        x_test = torch.tensor(dataset.x_test, dtype=torch.float32)
        y_test = torch.tensor(dataset.y_test, dtype=torch.long)

        train_loader = DataLoader(
            TensorDataset(x_train, y_train),
            batch_size=params.batch_size,
            shuffle=True,
        )
        test_loader = DataLoader(
            TensorDataset(x_test, y_test),
            batch_size=params.batch_size,
            shuffle=False,
        )

        model = ShapeClassifier(
            input_size=dataset.input_size,
            hidden_size=params.hidden_neurons,
            num_classes=CLASS_COUNT,
            activation=params.activation,
        ).to(self._device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self._learning_rate)

        loss_history: list[float] = self._train(model, train_loader, criterion, optimizer)
        accuracy: float = self._evaluate(model, test_loader)

        return ExperimentResult(
            hyper_parameters=params,
            accuracy=accuracy,
            loss_history=tuple(loss_history),
        )

    def _train(
        self,
        model: ShapeClassifier,
        loader: DataLoader[tuple[torch.Tensor, ...]],
        criterion: nn.Module,
        optimizer: optim.Optimizer,
    ) -> list[float]:
        model.train()
        history: list[float] = []

        for _epoch in range(self._epochs):
            running_loss: float = 0.0
            sample_count: int = 0

            for x_batch, y_batch in loader:
                inputs: torch.Tensor = x_batch.to(self._device)
                targets: torch.Tensor = y_batch.to(self._device)

                optimizer.zero_grad()
                outputs: torch.Tensor = model(inputs)
                loss: torch.Tensor = criterion(outputs, targets)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                sample_count += inputs.size(0)

            history.append(running_loss / sample_count)

        return history

    @torch.no_grad()
    def _evaluate(
        self,
        model: ShapeClassifier,
        loader: DataLoader[tuple[torch.Tensor, ...]],
    ) -> float:
        model.eval()
        correct: int = 0
        total: int = 0

        for x_batch, y_batch in loader:
            inputs: torch.Tensor = x_batch.to(self._device)
            targets: torch.Tensor = y_batch.to(self._device)

            outputs: torch.Tensor = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += targets.size(0)
            correct += int((predicted == targets).sum().item())

        return correct / total if total > 0 else 0.0
