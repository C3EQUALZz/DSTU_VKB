from enum import StrEnum, unique


@unique
class ActivationType(StrEnum):
    """Supported activation functions for hidden layers."""

    RELU = "relu"
    LINEAR = "linear"


