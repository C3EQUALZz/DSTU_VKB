from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset
from fulla.domain.price_prediction.value_objects.regression_result import RegressionResult


class RegressionResultPresenter(Protocol):
    """Port for presenting regression experiment results to the user."""

    @abstractmethod
    def show_dataset_info(self, dataset: RegressionDataset) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_results(self, results: Sequence[RegressionResult]) -> None:
        raise NotImplementedError

