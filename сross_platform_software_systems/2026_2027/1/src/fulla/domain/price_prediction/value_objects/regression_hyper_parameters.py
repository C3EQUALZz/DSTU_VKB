from dataclasses import dataclass

from fulla.domain.common.errors.base import DomainFieldError
from fulla.domain.common.values.base import BaseValueObject
from fulla.domain.price_prediction.value_objects.regression_activation_type import RegressionActivationType


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class RegressionHyperParameters(BaseValueObject):
    """Immutable set of hyperparameters for a single regression experiment."""

    hidden_neurons: int
    num_hidden_layers: int
    activation: RegressionActivationType
    batch_size: int
    learning_rate: float

    def _validate(self) -> None:
        if self.hidden_neurons <= 0:
            msg = f"hidden_neurons must be positive, got {self.hidden_neurons}"
            raise DomainFieldError(msg)
        if self.num_hidden_layers <= 0:
            msg = f"num_hidden_layers must be positive, got {self.num_hidden_layers}"
            raise DomainFieldError(msg)
        if self.batch_size <= 0:
            msg = f"batch_size must be positive, got {self.batch_size}"
            raise DomainFieldError(msg)
        if self.learning_rate <= 0:
            msg = f"learning_rate must be positive, got {self.learning_rate}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return (
            f"neurons={self.hidden_neurons}, layers={self.num_hidden_layers}, "
            f"act={self.activation.value}, bs={self.batch_size}, lr={self.learning_rate}"
        )


