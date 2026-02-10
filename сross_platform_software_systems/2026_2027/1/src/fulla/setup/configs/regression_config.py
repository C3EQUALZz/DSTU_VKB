from pydantic import BaseModel, Field

from fulla.domain.price_prediction.value_objects.regression_activation_type import RegressionActivationType


class RegressionConfig(BaseModel):
    """Configuration for regression experiments (Task 2)."""

    epochs: int = Field(default=100, description="Number of training epochs per experiment")
    test_size: float = Field(default=0.2, description="Fraction of data used for testing")
    random_state: int = Field(default=42, description="Random seed for reproducibility")

    neurons_list: tuple[int, ...] = Field(
        default=(64, 128, 256),
        description="Hidden layer sizes to test",
    )
    hidden_layers_list: tuple[int, ...] = Field(
        default=(1, 2, 3),
        description="Number of hidden layers to test",
    )
    activations: tuple[RegressionActivationType, ...] = Field(
        default=(RegressionActivationType.RELU, RegressionActivationType.TANH),
        description="Activation functions to test",
    )
    batch_sizes: tuple[int, ...] = Field(
        default=(64, 256),
        description="Batch sizes to test",
    )
    learning_rates: tuple[float, ...] = Field(
        default=(0.001,),
        description="Learning rates to test",
    )

