from enum import StrEnum, unique


@unique
class RegressionActivationType(StrEnum):
    """Supported activation functions for hidden layers in regression networks."""

    RELU = "relu"
    TANH = "tanh"
    LEAKY_RELU = "leaky_relu"


