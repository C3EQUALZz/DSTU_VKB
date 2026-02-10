"""
Лабораторная работа №1
Тестирование полносвязной архитектуры искусственной нейронной сети

Задание: Классификация геометрических фигур (треугольник, круг, квадрат)
с использованием полносвязной нейронной сети (PyTorch).

Эксперименты:
  - Количество нейронов: 10, 100, 5000
  - Активационная функция: relu, linear
  - Размер batch_size: 10, 100, 1000
"""

import numpy as np
import torch
from dishka import make_container

from fulla.application.commands.shape_recognition.run_all_experiments import (
    RunAllExperimentsCommand,
    RunAllExperimentsCommandHandler,
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

    handler = container.get(RunAllExperimentsCommandHandler)

    handler(
        RunAllExperimentsCommand(
            neurons_list=config.training.neurons_list,
            activations=config.training.activations,
            batch_sizes=config.training.batch_sizes,
        ),
    )

    container.close()


if __name__ == "__main__":
    main()
