"""
Лабораторная работа №1

Найти вероятности появления всех символов в тексте, который представит пользователи.
Посчитать энтропию данного текста.
Вывести графики
"""

import logging
import time

import combined_languages.theory_of_information.backend.core as core_namespace
from combined_languages.theory_of_information.backend.fifth_semestr.first_laboratory.model import \
    Model

logger = logging.getLogger(__name__)


def main() -> None:
    while True:
        string = input("Введите текст для энтропии: ")
        regex = input("Введите паттерн для регулярного выражения: ")

        if regex.isspace():
            regex = None

        model = Model(string, regex)

        logger.info(model.calculate_entropy())
        time.sleep(0.5)


if __name__ == "__main__":
    core_namespace.setup_logger()
    main()
