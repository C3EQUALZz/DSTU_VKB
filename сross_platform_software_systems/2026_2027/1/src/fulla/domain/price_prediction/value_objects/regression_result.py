from dataclasses import dataclass

from fulla.domain.common.values.base import BaseValueObject
from fulla.domain.price_prediction.value_objects.regression_hyper_parameters import RegressionHyperParameters


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class RegressionResult(BaseValueObject):
    """Immutable result of a single regression experiment."""

    hyper_parameters: RegressionHyperParameters
    mse: float
    mae: float
    r2_score: float
    loss_history: tuple[float, ...]

    def _validate(self) -> None:
        pass

    def __str__(self) -> str:
        return (
            f"{self.hyper_parameters} → MSE={self.mse:.4f}, MAE={self.mae:.4f}, R²={self.r2_score:.4f}"
        )

