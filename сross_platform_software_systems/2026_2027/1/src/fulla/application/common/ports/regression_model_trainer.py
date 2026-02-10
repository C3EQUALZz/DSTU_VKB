from abc import abstractmethod
from typing import Protocol

from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset
from fulla.domain.price_prediction.value_objects.regression_hyper_parameters import RegressionHyperParameters
from fulla.domain.price_prediction.value_objects.regression_result import RegressionResult


class RegressionModelTrainer(Protocol):
    """Port for training a fully-connected regression neural network and evaluating it."""

    @abstractmethod
    def train_and_evaluate(
        self,
        dataset: RegressionDataset,
        params: RegressionHyperParameters,
    ) -> RegressionResult:
        raise NotImplementedError

