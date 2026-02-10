from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset
from fulla.domain.shape_recognition.value_objects.experiment_result import ExperimentResult


class ResultPresenter(Protocol):
    """Port for presenting experiment results to the user."""

    @abstractmethod
    def show_dataset_info(self, dataset: PreparedDataset) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_results(self, results: Sequence[ExperimentResult]) -> None:
        raise NotImplementedError

