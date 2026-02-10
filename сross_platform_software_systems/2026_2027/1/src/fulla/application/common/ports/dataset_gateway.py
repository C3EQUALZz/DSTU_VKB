from abc import abstractmethod
from typing import Protocol

from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset


class DatasetGateway(Protocol):
    """Port for loading and preparing the geometric shapes dataset."""

    @abstractmethod
    def load(self) -> PreparedDataset:
        raise NotImplementedError


