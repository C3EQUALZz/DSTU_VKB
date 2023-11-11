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


def first_question(s=None):
    """
    Напишите функцию возведения всех элементов матрицы в квадрат
    """
    return array ** 2


def second_question(s=None):
    """
    Напишите функцию возведения всех четных элементов в квадрат.
    """
    return np.where(array % 2 == 0, array ** 2, array)


def third_question(s=None):
    """
    Напишите функцию возведения в квадрат всех элементов меньше 5
    """
    return np.where(array < 5, array ** 2, array)


def fourth_question(s=None):
    """
    Напишите функцию возведения первых четырех строк в квадрат
    """
    array[:4] = np.square(array[:4])
    return array


def main():
    match input("Введите номер задания "):
        case "1":
            print(first_question())
        case "2":
            print(second_question())
        case "3":
            print(third_question())
        case "4":
            print(fourth_question())
        case _:
            print("Вы выбрали неверный номер ")


if __name__ == "__main__":
    main()
