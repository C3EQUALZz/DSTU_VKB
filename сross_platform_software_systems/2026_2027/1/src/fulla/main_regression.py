"""
Лабораторная работа №2
Прогнозирование целевого показателя с полносвязной архитектурой ИНС

Задание: Используя датасет California Housing реализовать ИНС,
выполняющую задачу прогнозирования цены недвижимости.
Добиться максимальной точности по метрике MSE.

Эксперименты:
  - Количество нейронов: 64, 128, 256
  - Количество скрытых слоёв: 1, 2, 3
  - Активационная функция: relu, tanh
  - Размер batch_size: 64, 256
  - Learning rate: 0.001
"""

import numpy as np
import torch
from dishka import make_container

from fulla.application.commands.price_prediction.run_regression_experiments import (
    RunRegressionExperimentsCommand,
    RunRegressionExperimentsCommandHandler,
)
from fulla.setup.configs.app_config import ApplicationConfig
from fulla.setup.configs.logging import configure_logging
from fulla.setup.ioc import setup_providers

RANDOM_STATE = 42


def main() -> None:
    config = ApplicationConfig()
    configure_logging(config.logging)

    torch.manual_seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)  # noqa: NPY002

    container = make_container(
        *setup_providers(),
        context={ApplicationConfig: config},
    )

    handler = container.get(RunRegressionExperimentsCommandHandler)

    handler(
        RunRegressionExperimentsCommand(
            neurons_list=config.regression.neurons_list,
            hidden_layers_list=config.regression.hidden_layers_list,
            activations=config.regression.activations,
            batch_sizes=config.regression.batch_sizes,
            learning_rates=config.regression.learning_rates,
        ),
    )

    container.close()


if __name__ == "__main__":
    main()


