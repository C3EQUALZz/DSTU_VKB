import logging
from typing import Final, final

import numpy as np
import numpy.typing as npt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset

logger: Final[logging.Logger] = logging.getLogger(__name__)


@final
class CaliforniaHousingGateway:
    """Loads the California Housing dataset from scikit-learn, applies standard scaling, and splits train/test."""

    def __init__(
        self,
        test_size: float,
        random_state: int,
    ) -> None:
        self._test_size: Final[float] = test_size
        self._random_state: Final[int] = random_state
        self._cache: RegressionDataset | None = None

    def load(self) -> RegressionDataset:
        if self._cache is not None:
            return self._cache

        data = fetch_california_housing()
        x_all: npt.NDArray[np.float64] = data.data  # type: ignore[assignment]
        y_all: npt.NDArray[np.float64] = data.target  # type: ignore[assignment]
        feature_names: tuple[str, ...] = tuple(data.feature_names)  # type: ignore[arg-type]

        x_train_raw, x_test_raw, y_train_raw, y_test_raw = train_test_split(
            x_all,
            y_all,
            test_size=self._test_size,
            random_state=self._random_state,
        )

        # Standardize features for better NN convergence
        scaler = StandardScaler()
        x_train_scaled: npt.NDArray[np.float32] = scaler.fit_transform(x_train_raw).astype(np.float32)
        x_test_scaled: npt.NDArray[np.float32] = scaler.transform(x_test_raw).astype(np.float32)

        self._cache = RegressionDataset(
            x_train=x_train_scaled,
            y_train=y_train_raw.astype(np.float32),
            x_test=x_test_scaled,
            y_test=y_test_raw.astype(np.float32),
            feature_names=feature_names,
        )

        logger.info(
            "California Housing dataset loaded: %d train, %d test samples (features=%d)",
            self._cache.train_count,
            self._cache.test_count,
            self._cache.input_size,
        )

        return self._cache


