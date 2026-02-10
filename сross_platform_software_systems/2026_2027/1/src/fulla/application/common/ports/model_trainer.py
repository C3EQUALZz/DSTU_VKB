from abc import abstractmethod
from typing import Protocol

from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset
from fulla.domain.shape_recognition.value_objects.experiment_result import ExperimentResult
from fulla.domain.shape_recognition.value_objects.hyper_parameters import HyperParameters


class ModelTrainer(Protocol):
    """Port for training a fully-connected neural network and evaluating it."""

    @abstractmethod
    def train_and_evaluate(
        self,
        dataset: PreparedDataset,
        params: HyperParameters,
    ) -> ExperimentResult:
        raise NotImplementedError

