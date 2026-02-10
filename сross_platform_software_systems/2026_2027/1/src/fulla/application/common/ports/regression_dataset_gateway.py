from abc import abstractmethod
from typing import Protocol

from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset


class RegressionDatasetGateway(Protocol):
    """Port for loading and preparing a tabular regression dataset."""

    @abstractmethod
    def load(self) -> RegressionDataset:
        raise NotImplementedError

