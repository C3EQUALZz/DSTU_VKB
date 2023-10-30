"""
Выполнил Ковалев Данил ВКБ22
Лабораторная 2
Для булевой функции от трех переменных вычислите матрицы:
a) перехода от таблицы к многочлену Жегалкина и обратную (получить полином Жегалкина с помощью БМФ)
"""
from functools import wraps
from itertools import pairwise, product, compress

import numpy as np
from prettytable import PrettyTable


def counter(func):
    """
    Декоратор, который подсчитывает сколько раз мы вызвали функцию.
    Для вывода номера строки нужен
    """

    @wraps(func)
    def inner(*args, **kwargs):
        inner.count += 1
        return func(*args, **kwargs)

    inner.count = 0
    return inner


class Polynom:
    def __init__(self, vector: list) -> None:
        self.vector: list = vector
        self.result: list = [self._vector[0]]
        self.table_without_vector = np.array([list(x) for x in product([0, 1], repeat=3)])
        self.table = self.create_table().transpose()

    @property
    def vector(self) -> list:
        return self._vector

    @vector.setter
    def vector(self, vec) -> None:
        if len(vec) % 2 != 0 or len(vec) % 6 == 0:
            raise ValueError("Ввели неправильный вектор по длине ")
        if not all(map(lambda x: 0 <= x <= 1, vec)):
            raise ValueError("Функция может содержать только 0 и 1")
        self._vector = vec

    def get_polynom_triangle(self) -> list:
        """
        Здесь мы получаем коэффициенты для
        """
        while len(current_row := self.__xor_elements()) > 0:
            self.result.append(current_row[0])
        return self.result

    @counter
    def __xor_elements(self) -> list:
        """
        Метод, который проводит xor попарно между элементами
        """
        print(f"{self.__xor_elements.count} строка треугольника -  {' '.join(map(str, self._vector)):^20}")
        self._vector = [x ^ y for x, y in pairwise(self._vector)]
        return self._vector

    def create_table(self):
        """
        Метод, который вставляет функцию f в numpy матрицу
        """
        return np.insert(self.table_without_vector, 3, np.array(self._vector), axis=1)

    def print_polynom(self) -> None:
        res = ''
        for value, raw in zip(self.get_polynom_triangle(), self.table_without_vector):
            if value == 1:
                res += " xor " + ''.join(compress(("x", "y", "z"), raw))
        print(f"Результат полинома Жегалкина - {res.strip(' xor ')}")

    def print_table(self) -> None:
        table = PrettyTable()
        table.field_names = ("x", "y", "z", "f")
        table.add_rows(self.create_table())
        print("Все булевы строки матрицы: ", table, sep='\n')


def main() -> None:
    s = list(map(int, input("Введите функцию - вектор для Полинома Жегалкина ").split()))
    result = Polynom(s)
    result.print_table()
    result.print_polynom()
    print(f"Транспонированная матрица: \n\n {result.table}")


if __name__ == "__main__":
    main()

# 0 1 1 1 0 0 1 1
