"""
Лабораторная работа «Реализация алгоритмов кодирования Лемпеля-Зива: LZ77, LZ78»
Входные данные: какой-то текст или набор символов (и русские буквы, и латиница, а также все знаки препинания и пробелы).
Выходные данные: таблица пакетов и их содержания.
Задача: реализовать алгоритмы кодирования Лемпеля-Зива: LZ77, LZ78.

Требования к языку не предъявляются (только не паскаль, делфи и не вба).

ВАЖНО! Программа должна решать общие случаи, а не частные (любой текст, любой язык).
Допустимо буквы приводить к одному регистру.

На положительные баллы (от 61 до 90, если мы говорим о 100-бальной системе) программа должна решать общие случаи,
а не частные (любой текст, любой язык).
Допустимо буквы приводить к одному регистру.
Для получения 91 балла и выше – ещё реализуете интерфейс.
"""
import time
import logging
import python_language.theory_of_information.core as core_namespace
from python_language.theory_of_information.models.second_laboratory import LZ77, TokenLZ77, LZ78, TokenLZ78
from python_language.theory_of_information.models.second_laboratory.utils import create_table

logger = logging.getLogger(__name__)


def lz77_encode(data: str) -> str:
    algorithm = LZ77()
    compressed_text = algorithm.compress(data)
    return "\n" + str(create_table(compressed_text, data))


def lz77_decode(data: str) -> str:
    algorithm = LZ77()
    prepared_data = [TokenLZ77(*package) for package in eval(data)]
    return str(algorithm.decompress(prepared_data))


def lz78_encode(data: str) -> str:
    algorithm = LZ78()
    compressed_text = algorithm.compress(data)
    return "\n" + str(create_table(compressed_text, data))


def lz78_decode(data: str) -> str:
    algorithm = LZ78()
    prepared_data = [TokenLZ78(*package) for package in eval(data)]
    return str(algorithm.decompress(prepared_data))


def main() -> None:
    algorithms = {
        "1": {"name": "LZ77", "encode": lz77_encode, "decode": lz77_decode},
        "2": {"name": "LZ78", "encode": lz78_encode, "decode": lz78_decode},
    }

    while True:
        algo_choice = input("Какой из 2 алгоритмов вы хотите использовать? LZ77(1) или LZ78(2)? ")
        if algo_choice not in algorithms:
            logger.warning("Неверный выбор, попробуйте снова.")
            continue

        action_choice = input("Выберите действие: зашифровать(1) или расшифровать(2)? ")
        if action_choice not in {"1", "2"}:
            logger.warning("Неверный выбор, попробуйте снова.")
            continue

        algorithm = algorithms[algo_choice]
        if action_choice == "1":
            data = input("Введите слово или предложение (пример: ababcbababaa): ")
            result = algorithm["encode"](data)
            logger.info(f"Результат кодирования {algorithm['name']}: {result}")
        else:
            data = input("Введите набор кортежей"
                         " (пример: [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (2, 2, 'a')]): ")
            result = algorithm["decode"](data)
            logger.info(f"Результат декодирования {algorithm['name']}: {result}")

        time.sleep(0.5)


if __name__ == "__main__":
    core_namespace.setup_logger()
    main()
