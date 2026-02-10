from dataclasses import dataclass

from fulla.domain.common.errors.base import DomainFieldError
from fulla.domain.common.values.base import BaseValueObject
from fulla.domain.shape_recognition.value_objects.activation_type import ActivationType


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class HyperParameters(BaseValueObject):
    """Immutable set of hyperparameters for a single experiment run."""

    hidden_neurons: int
    activation: ActivationType
    batch_size: int

    def _validate(self) -> None:
        if self.hidden_neurons <= 0:
            msg = f"hidden_neurons must be positive, got {self.hidden_neurons}"
            raise DomainFieldError(msg)
        if self.batch_size <= 0:
            msg = f"batch_size must be positive, got {self.batch_size}"
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"neurons={self.hidden_neurons}, activation={self.activation.value}, batch_size={self.batch_size}"

