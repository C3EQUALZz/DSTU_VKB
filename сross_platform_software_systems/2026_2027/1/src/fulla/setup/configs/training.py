from pydantic import BaseModel, Field

from fulla.domain.shape_recognition.value_objects.activation_type import ActivationType


class TrainingConfig(BaseModel):
    """Configuration for training experiments."""

    epochs: int = Field(default=30, description="Number of training epochs per experiment")
    learning_rate: float = Field(default=0.001, description="Adam optimizer learning rate")
    test_size: float = Field(default=0.2, description="Fraction of data used for testing")
    random_state: int = Field(default=42, description="Random seed for reproducibility")
    img_height: int = Field(default=20, description="Height of loaded images in pixels")
    img_width: int = Field(default=20, description="Width of loaded images in pixels")
    dataset_url: str = Field(
        default="https://storage.yandexcloud.net/aiueducation/Content/base/l3/hw_light.zip",
        description="URL to download the dataset archive",
    )
    data_dir: str = Field(default="hw_light", description="Local directory for extracted dataset")
    neurons_list: tuple[int, ...] = Field(default=(10, 100, 5000), description="Hidden layer sizes to test")
    activations: tuple[ActivationType, ...] = Field(
        default=(ActivationType.RELU, ActivationType.LINEAR),
        description="Activation functions to test",
    )
    batch_sizes: tuple[int, ...] = Field(default=(10, 100, 1000), description="Batch sizes to test")


