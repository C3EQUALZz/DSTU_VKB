"""
В данном модуле описаны вспомогательные функции для вывода таблиц на печать
"""
__all__ = ["generate_table", "append"]
#####################################################################
import numpy as np
from prettytable import PrettyTable


###################################################################

def generate_table(array: np.ndarray) -> PrettyTable:
    """
    Функция, которая создает таблицу, служит интерфейсом для взаимодействия
    """
    table = PrettyTable()

    match type(array[0]).__name__:
        case "Student":
            table.field_names = ["Фамилия", "Инициалы", "Номер группы", "Оценки", "Средний балл"]
            _generate_table_students(table=table, students=array)

        case "Train":
            table.field_names = ["Номер поезда", "Пункт назначения", "Время отправления"]
            _generate_table_trains(table=table, trains=array)

    return table


def _generate_table_students(table: PrettyTable, students: np.ndarray) -> None:
    """
    Функция, которая печатает таблицу со студентами
    """
    # создаем массив со средними баллами, чтобы можно было сделать сортировку
    sorting_key = [np.mean(student.grades) for student in students]
    # получаем индексы, как мы будем сортировать (по умолчанию идет по возрастанию
    sorting_indexes = np.argsort(sorting_key)
    # добавляем в таблицу все наши значения
    table.add_rows(
        [
            student.last_name,
            student.initials,
            student.number_group,
            ', '.join(map(str, student.grades)),
            np.mean(student.grades).round(3)
        ]
        for student in students[sorting_indexes]
    )


def _generate_table_trains(table: PrettyTable, trains: np.ndarray) -> None:
    """
    Функция, которая печатает таблицу с поездами
    """
    table.add_rows([train.number, train.dest, train.departure] for train in trains)

def append():
    ...
