from collections.abc import Iterable

import torch
from dishka import Provider, Scope, provide

from fulla.application.commands.price_prediction.run_regression_experiments import (
    RunRegressionExperimentsCommandHandler,
)
from fulla.application.commands.shape_recognition.run_all_experiments import RunAllExperimentsCommandHandler
from fulla.application.commands.shape_recognition.run_experiment import RunExperimentCommandHandler
from fulla.application.common.ports.dataset_gateway import DatasetGateway
from fulla.application.common.ports.model_trainer import ModelTrainer
from fulla.application.common.ports.regression_dataset_gateway import RegressionDatasetGateway
from fulla.application.common.ports.regression_model_trainer import RegressionModelTrainer
from fulla.application.common.ports.regression_result_presenter import RegressionResultPresenter
from fulla.application.common.ports.result_presenter import ResultPresenter
from fulla.infrastructure.adapters.dataset.california_housing_gateway import CaliforniaHousingGateway
from fulla.infrastructure.adapters.dataset.yandex_cloud_dataset_gateway import YandexCloudDatasetGateway
from fulla.infrastructure.adapters.model.pytorch_model_trainer import PyTorchModelTrainer
from fulla.infrastructure.adapters.model.pytorch_regression_trainer import PyTorchRegressionTrainer
from fulla.infrastructure.adapters.visualization.matplotlib_result_presenter import MatplotlibResultPresenter
from fulla.infrastructure.adapters.visualization.regression_result_presenter import MatplotlibRegressionResultPresenter
from fulla.setup.configs.app_config import ApplicationConfig


class ConfigsProvider(Provider):
    scope = Scope.APP

    config = provide(source=ApplicationConfig, provides=ApplicationConfig)


class InfrastructureProvider(Provider):
    """Provides infrastructure adapters for Task 1 (classification)."""

    scope = Scope.APP

    @provide(provides=DatasetGateway)
    def dataset_gateway(self, config: ApplicationConfig) -> YandexCloudDatasetGateway:
        cfg = config.training
        return YandexCloudDatasetGateway(
            dataset_url=cfg.dataset_url,
            data_dir=cfg.data_dir,
            img_height=cfg.img_height,
            img_width=cfg.img_width,
            test_size=cfg.test_size,
            random_state=cfg.random_state,
        )

    @provide(provides=ModelTrainer)
    def model_trainer(self, config: ApplicationConfig) -> PyTorchModelTrainer:
        cfg = config.training
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return PyTorchModelTrainer(
            epochs=cfg.epochs,
            learning_rate=cfg.learning_rate,
            device=device,
        )

    result_presenter = provide(source=MatplotlibResultPresenter, provides=ResultPresenter)


class RegressionInfrastructureProvider(Provider):
    """Provides infrastructure adapters for Task 2 (regression)."""

    scope = Scope.APP

    @provide(provides=RegressionDatasetGateway)
    def regression_dataset_gateway(self, config: ApplicationConfig) -> CaliforniaHousingGateway:
        cfg = config.regression
        return CaliforniaHousingGateway(
            test_size=cfg.test_size,
            random_state=cfg.random_state,
        )

    @provide(provides=RegressionModelTrainer)
    def regression_model_trainer(self, config: ApplicationConfig) -> PyTorchRegressionTrainer:
        cfg = config.regression
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return PyTorchRegressionTrainer(
            epochs=cfg.epochs,
            device=device,
        )

    regression_result_presenter = provide(
        source=MatplotlibRegressionResultPresenter,
        provides=RegressionResultPresenter,
    )


class InteractorsProvider(Provider):
    scope = Scope.APP

    run_experiment = provide(RunExperimentCommandHandler)
    run_all_experiments = provide(RunAllExperimentsCommandHandler)
    run_regression_experiments = provide(RunRegressionExperimentsCommandHandler)


def setup_providers() -> Iterable[Provider]:
    return (
        ConfigsProvider(),
        InfrastructureProvider(),
        RegressionInfrastructureProvider(),
        InteractorsProvider(),
    )
