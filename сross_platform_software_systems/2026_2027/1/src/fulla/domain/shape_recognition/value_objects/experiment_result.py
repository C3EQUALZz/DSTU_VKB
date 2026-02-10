from dataclasses import dataclass

from fulla.domain.common.values.base import BaseValueObject
from fulla.domain.shape_recognition.value_objects.hyper_parameters import HyperParameters


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class ExperimentResult(BaseValueObject):
    """Immutable result of a single training experiment."""

    hyper_parameters: HyperParameters
    accuracy: float
    loss_history: tuple[float, ...]

    def _validate(self) -> None:
        pass

    @property
    def accuracy_percent(self) -> float:
        return round(self.accuracy * 100, 2)

    def __str__(self) -> str:
        return f"{self.hyper_parameters} → accuracy={self.accuracy_percent:.2f}%"


