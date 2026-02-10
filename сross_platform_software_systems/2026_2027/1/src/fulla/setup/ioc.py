from collections.abc import Iterable

import torch
from dishka import Provider, Scope, provide

from fulla.application.commands.shape_recognition.run_all_experiments import RunAllExperimentsCommandHandler
from fulla.application.commands.shape_recognition.run_experiment import RunExperimentCommandHandler
from fulla.application.common.ports.dataset_gateway import DatasetGateway
from fulla.application.common.ports.model_trainer import ModelTrainer
from fulla.application.common.ports.result_presenter import ResultPresenter
from fulla.infrastructure.adapters.dataset.yandex_cloud_dataset_gateway import YandexCloudDatasetGateway
from fulla.infrastructure.adapters.model.pytorch_model_trainer import PyTorchModelTrainer
from fulla.infrastructure.adapters.visualization.matplotlib_result_presenter import MatplotlibResultPresenter
from fulla.setup.configs.app_config import ApplicationConfig


class ConfigsProvider(Provider):
    scope = Scope.APP

    config = provide(source=ApplicationConfig, provides=ApplicationConfig)


class InfrastructureProvider(Provider):
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


class InteractorsProvider(Provider):
    scope = Scope.APP

    run_experiment = provide(RunExperimentCommandHandler)
    run_all_experiments = provide(RunAllExperimentsCommandHandler)


def setup_providers() -> Iterable[Provider]:
    return (
        ConfigsProvider(),
        InfrastructureProvider(),
        InteractorsProvider(),
    )
