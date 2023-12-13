"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

import numpy as np

array = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [2, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2],
        [1, 3, 5, 7, 9, 7, 5, 3],
        [3, 1, 5, 3, 2, 6, 5, 7],
        [1, 7, 5, 9, 7, 3, 1, 5],
        [2, 6, 3, 5, 1, 7, 3, 2]
    ], dtype=np.uint8
)


def first_var_first_question(s=None) -> np.ndarray:
    """
    Напишите функцию возведения всех элементов матрицы в квадрат
    Ничего вводить не надо
    """
    return array ** 2


def second_var_first_question(s=None) -> np.ndarray:
    """
    Напишите функцию нахождения суммы по элементам строк
    Ничего вводить не надо
    """
    # axis = 0 (столбец), axis = 1 (строка), axis = 2 (ширина, если большая мерность) и т.д.
    return np.sum(array, axis=1)


def third_var_first_question(s=None) -> np.ndarray:
    """
    Напишите функцию возведения в квадрат всех элементов, которые находятся в четных столбцах.
    Ничего вводить не надо
    """
    array[:, ::2] = array[:, ::2] ** 2
    return array


def fourth_var_first_question(k=None) -> np.ndarray:
    """
    Напишите функцию умножения по строкам.
    Ничего вводить не надо
    """
    return np.prod(array, axis=1)


def fifth_var_first_question(k=None) -> np.ndarray:
    """
    Напишите функцию замены всех четных элементов матрицы на 0
    Ничего вводить не надо
    """
    return np.where(array % 2 == 0, 0, array)


def sixth_var_first_question(ind: str) -> np.ndarray | str:
    """
    Пусть пользователь через консоль вводит число.
    Напишите функцию удаления строки в матрице, чей номер равен введенному числу.
    Пример ввода: 0
    """
    try:
        return np.delete(array, int(ind), axis=0)
    except IndexError:
        return "Недопустимый индекс"


def seventh_var_first_question(k=None) -> np.ndarray:
    """
    Напишете функцию, которая поменяет первую и последнюю строку матрицы местами.
    Ничего вводить не надо
    """
    array[[0, len(array) - 1]] = array[[len(array) - 1, 0]]
    return array


def eight_var_first_question(data: str) -> np.ndarray:
    """
    Пусть пользователь через консоль вводит два числа: первое - номер строки,
    второе - номер столбца. Напишите функцию, которая найдет число в данной позиции.
    Пример ввода: 0 1
    """
    string, column = map(int, data.split())
    return array[string, column]


def main():
    match input("Введите номер задания "):
        case "1":
            print(first_var_first_question())
        case "2":
            print(second_var_first_question())
        case "3":
            print(third_var_first_question())
        case "4":
            print(fourth_var_first_question())
        case "5":
            print(fifth_var_first_question())
        case "6":
            print(sixth_var_first_question(input("Введите индекс строки, которую хотите удалить ")))
        case "7":
            print(seventh_var_first_question())
        case "8":
            print(eight_var_first_question(input("Введите два числа через пробел ")))
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
