"""
Данный модуль разработан, чтобы описывать логику декораторов.
"""

__all__ = ["progress_bar", "pprint_matrix", "retry_on_value_error"]

from time import sleep

from colorama import Fore, Style
from terminaltables import DoubleTable
from tqdm import tqdm

comments = (
    Style.BRIGHT
    + Fore.GREEN
    + f"\N{SNAKE} Работу выполнил: Ковалев Данил ВКБ12 \N{SNAKE}\nПриветствую "
    f"пользователя ^_^\nДанный скрипт направлен на реализацию алгоритма "
    f"Флойда.\nЕсли хотите посмотреть реализацию в реальных задачах, то перейдите "
    f"в другую папки 'Примеры Флойда', в ином случае:\nначинайте с этого файла."
)


def progress_bar(func):
    """
    Функция - декоратор для создания прогресс бара.
    Делает так, чтобы программа останавливалась на 5 с, показывая прогресс бар в консоли.
    Не измеряет само время выполнения программы, только красивая анимация для взаимодействия.
    :param func: Любая функция.
    :return: Результат действия функции
    """

    def wrapper(*args, **kwargs):
        print(comments)
        for _ in tqdm(range(100)):
            sleep(0.05)
        return func(*args, **kwargs)

    return wrapper


def retry_on_value_error(func):
    """
    Функция - декоратор для проверки на ошибки функции.
    В случае чего перезапускает функцию, если неверно ввели данные.
    :param func: Любая функция, где может произойти ValueError.
    :return: Результат действия функции в случае успешного выполнения.
    """

    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except ValueError:
                print("Ошибка! Попробуйте еще раз.")

    return wrapper


def pprint_matrix(func):
    """
    Функция - декоратор, которая распечатывает матрицу, если функция возвращает её.
    Если вам нужно распечатать матрицу, то надо поставить вторым аргументом.
    :param func: Любая функция, где требуется распечатать матрицу.
    :return: Результат действия функции.
    """

    def inner(*args, **kwargs):
        if isinstance(result := func(*args, **kwargs), tuple):
            _, matrix = result
        else:
            matrix = result
        table_data = [[" "] + [chr(x + 65) for x in range(len(matrix))]]
        table_data.extend(
            [(chr(number + 65), *raw) for number, raw in enumerate(matrix)]
        )
        table_instance = DoubleTable(table_data, "Матрица=смежности")
        print("\n" + table_instance.table, "\n", sep="")
        return result

    return inner
