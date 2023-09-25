"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""
import numpy as np


def first_question(n):
    """
    Пусть дана матрица чисел размером NxN. Представьте данную матрицу в виде списка.
    """
    matrix = np.random.randint(1000, size=(3, 3))
    print("Наша матрица: ", np.matrix(matrix), f"Cумма: {matrix.sum()}", sep='\n')

    linear = lambda data: [data] if isinstance(data, np.int64) else sum(map(linear, data), [])
    print(f"Представление данной матрицы в виде строки: {linear(matrix)}")


def second_question(lst: list, for_add: str):
    """
    Пусть дан список из десяти элементов.
    Вариант 1. Удалите первые 2 элемента и добавьте 2 новых. Выведите список на экран
    """
    print(f"До: {lst}", f"После:{lst[2:] + for_add.split()}", sep='\n')


def third_question():
    ...
