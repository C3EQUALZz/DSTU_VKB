import logging
from typing import Final, final

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset
from fulla.domain.price_prediction.value_objects.regression_hyper_parameters import RegressionHyperParameters
from fulla.domain.price_prediction.value_objects.regression_result import RegressionResult
from fulla.infrastructure.adapters.model.regression_network import RegressionNetwork

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class PyTorchRegressionTrainer:
    """Trains a RegressionNetwork and evaluates it using PyTorch with MSE loss."""

    def __init__(
        self,
        epochs: int,
        device: torch.device,
    ) -> None:
        self._epochs: Final[int] = epochs
        self._device: Final[torch.device] = device

    def train_and_evaluate(
        self,
        dataset: RegressionDataset,
        params: RegressionHyperParameters,
    ) -> RegressionResult:
        x_train = torch.tensor(dataset.x_train, dtype=torch.float32)
        y_train = torch.tensor(dataset.y_train, dtype=torch.float32)
        x_test = torch.tensor(dataset.x_test, dtype=torch.float32)
        y_test = torch.tensor(dataset.y_test, dtype=torch.float32)

        train_loader = DataLoader(
            TensorDataset(x_train, y_train),
            batch_size=params.batch_size,
            shuffle=True,
        )

        model = RegressionNetwork(
            input_size=dataset.input_size,
            hidden_size=params.hidden_neurons,
            num_hidden_layers=params.num_hidden_layers,
            activation=params.activation,
        ).to(self._device)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=params.learning_rate)

        loss_history: list[float] = self._train(model, train_loader, criterion, optimizer)
        mse, mae, r2 = self._evaluate(model, x_test, y_test)

        return RegressionResult(
            hyper_parameters=params,
            mse=mse,
            mae=mae,
            r2_score=r2,
            loss_history=tuple(loss_history),
        )

    def _train(
        self,
        model: RegressionNetwork,
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
                predictions: torch.Tensor = model(inputs)
                loss: torch.Tensor = criterion(predictions, targets)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                sample_count += inputs.size(0)

            history.append(running_loss / sample_count)

        return history

    @torch.no_grad()
    def _evaluate(
        self,
        model: RegressionNetwork,
        x_test: torch.Tensor,
        y_test: torch.Tensor,
    ) -> tuple[float, float, float]:
        """Evaluate the model and return (MSE, MAE, R²)."""
        model.eval()

        inputs = x_test.to(self._device)
        targets = y_test.to(self._device)
        predictions: torch.Tensor = model(inputs)

        residuals = predictions - targets
        mse: float = float(residuals.pow(2).mean().item())
        mae: float = float(residuals.abs().mean().item())

        # R² = 1 - SS_res / SS_tot
        ss_res: float = float(residuals.pow(2).sum().item())
        ss_tot: float = float((targets - targets.mean()).pow(2).sum().item())
        r2: float = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

        return mse, mae, r2

