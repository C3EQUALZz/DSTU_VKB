import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from fulla.application.common.ports.dataset_gateway import DatasetGateway
from fulla.application.common.ports.model_trainer import ModelTrainer
from fulla.domain.shape_recognition.value_objects.experiment_result import ExperimentResult
from fulla.domain.shape_recognition.value_objects.hyper_parameters import HyperParameters

if TYPE_CHECKING:
    from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RunExperimentCommand:
    """Command to run a single experiment with given hyperparameters."""

    hyper_parameters: HyperParameters


@final
class RunExperimentCommandHandler:
    def __init__(
        self,
        dataset_gateway: DatasetGateway,
        model_trainer: ModelTrainer,
    ) -> None:
        self._dataset_gateway: Final[DatasetGateway] = dataset_gateway
        self._model_trainer: Final[ModelTrainer] = model_trainer

    def __call__(self, data: RunExperimentCommand) -> ExperimentResult:
        logger.info("Running experiment: %s", data.hyper_parameters)

        dataset: PreparedDataset = self._dataset_gateway.load()
        result: ExperimentResult = self._model_trainer.train_and_evaluate(dataset, data.hyper_parameters)

        logger.info("Experiment done: accuracy=%.4f", result.accuracy)
        return result
