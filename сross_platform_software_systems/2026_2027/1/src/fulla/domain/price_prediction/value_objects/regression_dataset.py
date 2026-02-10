from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True, slots=True)
class RegressionDataset:
    """Holds train/test split of tabular data for a regression task."""

    x_train: npt.NDArray[np.float32]
    y_train: npt.NDArray[np.float32]
    x_test: npt.NDArray[np.float32]
    y_test: npt.NDArray[np.float32]
    feature_names: tuple[str, ...]

    @property
    def input_size(self) -> int:
        return int(self.x_train.shape[1])

    @property
    def train_count(self) -> int:
        return int(self.x_train.shape[0])

    @property
    def test_count(self) -> int:
        return int(self.x_test.shape[0])


