import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, final

from fulla.application.common.ports.regression_dataset_gateway import RegressionDatasetGateway
from fulla.application.common.ports.regression_model_trainer import RegressionModelTrainer
from fulla.application.common.ports.regression_result_presenter import RegressionResultPresenter
from fulla.domain.price_prediction.value_objects.regression_activation_type import RegressionActivationType
from fulla.domain.price_prediction.value_objects.regression_hyper_parameters import RegressionHyperParameters
from fulla.domain.price_prediction.value_objects.regression_result import RegressionResult

if TYPE_CHECKING:
    from fulla.domain.price_prediction.value_objects.regression_dataset import RegressionDataset

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RunRegressionExperimentsCommand:
    """Command to run the full hyperparameter grid search for regression."""

    neurons_list: tuple[int, ...]
    hidden_layers_list: tuple[int, ...]
    activations: tuple[RegressionActivationType, ...]
    batch_sizes: tuple[int, ...]
    learning_rates: tuple[float, ...]


@final
class RunRegressionExperimentsCommandHandler:
    def __init__(
        self,
        dataset_gateway: RegressionDatasetGateway,
        model_trainer: RegressionModelTrainer,
        result_presenter: RegressionResultPresenter,
    ) -> None:
        self._dataset_gateway: Final[RegressionDatasetGateway] = dataset_gateway
        self._model_trainer: Final[RegressionModelTrainer] = model_trainer
        self._result_presenter: Final[RegressionResultPresenter] = result_presenter

    def __call__(self, data: RunRegressionExperimentsCommand) -> Sequence[RegressionResult]:
        dataset: RegressionDataset = self._dataset_gateway.load()
        self._result_presenter.show_dataset_info(dataset)

        total: int = (
            len(data.neurons_list)
            * len(data.hidden_layers_list)
            * len(data.activations)
            * len(data.batch_sizes)
            * len(data.learning_rates)
        )
        results: list[RegressionResult] = []
        exp_num: int = 0

        for neurons in data.neurons_list:
            for num_layers in data.hidden_layers_list:
                for activation in data.activations:
                    for batch_size in data.batch_sizes:
                        for lr in data.learning_rates:
                            exp_num += 1
                            params = RegressionHyperParameters(
                                hidden_neurons=neurons,
                                num_hidden_layers=num_layers,
                                activation=activation,
                                batch_size=batch_size,
                                learning_rate=lr,
                            )

                            logger.info("[%d/%d] %s", exp_num, total, params)

                            result: RegressionResult = self._model_trainer.train_and_evaluate(
                                dataset, params,
                            )
                            results.append(result)

                            logger.info(
                                "[%d/%d] MSE=%.4f, MAE=%.4f, R²=%.4f",
                                exp_num, total, result.mse, result.mae, result.r2_score,
                            )

        self._result_presenter.show_results(results)
        return results


