import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from fulla.application.common.ports.dataset_gateway import DatasetGateway
from fulla.application.common.ports.model_trainer import ModelTrainer
from fulla.application.common.ports.result_presenter import ResultPresenter
from fulla.domain.shape_recognition.value_objects.activation_type import ActivationType
from fulla.domain.shape_recognition.value_objects.experiment_result import ExperimentResult
from fulla.domain.shape_recognition.value_objects.hyper_parameters import HyperParameters

if TYPE_CHECKING:
    from fulla.domain.shape_recognition.value_objects.dataset import PreparedDataset

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RunAllExperimentsCommand:
    """Command to run the full hyperparameter grid search."""

    neurons_list: tuple[int, ...]
    activations: tuple[ActivationType, ...]
    batch_sizes: tuple[int, ...]


@final
class RunAllExperimentsCommandHandler:
    def __init__(
        self,
        dataset_gateway: DatasetGateway,
        model_trainer: ModelTrainer,
        result_presenter: ResultPresenter,
    ) -> None:
        self._dataset_gateway: Final[DatasetGateway] = dataset_gateway
        self._model_trainer: Final[ModelTrainer] = model_trainer
        self._result_presenter: Final[ResultPresenter] = result_presenter

    def __call__(self, data: RunAllExperimentsCommand) -> Sequence[ExperimentResult]:
        dataset: PreparedDataset = self._dataset_gateway.load()
        self._result_presenter.show_dataset_info(dataset)

        total: int = len(data.neurons_list) * len(data.activations) * len(data.batch_sizes)
        results: list[ExperimentResult] = []
        exp_num: int = 0

        for neurons in data.neurons_list:
            for activation in data.activations:
                for batch_size in data.batch_sizes:
                    exp_num += 1
                    params = HyperParameters(
                        hidden_neurons=neurons,
                        activation=activation,
                        batch_size=batch_size,
                    )

                    logger.info("[%d/%d] %s", exp_num, total, params)

                    result: ExperimentResult = self._model_trainer.train_and_evaluate(dataset, params)
                    results.append(result)

                    logger.info("[%d/%d] accuracy = %.4f", exp_num, total, result.accuracy)

        self._result_presenter.show_results(results)
        return results
