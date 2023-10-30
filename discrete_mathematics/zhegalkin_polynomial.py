"""
Выполнил Ковалев Данил ВКБ22
Лабораторная 2
Для булевой функции от трех переменных вычислите матрицы:
a) перехода от таблицы к многочлену Жегалкина и обратную (получить полином Жегалкина с помощью БПФ)
Пример для ввода: 0 1 1 1 0 0 1 1
"""
from functools import wraps
from itertools import pairwise, product, compress, islice

import numpy as np
from prettytable import PrettyTable
from math import log2


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
    def __init__(self, vector: list[int, ...]) -> None:
        """
        Args:
            vector (list): наша булева функция
            table_without
        """
        self.vector: list = vector
        self.table = np.array([list(x) for x in product([0, 1], repeat=3)])

    @property
    def vector(self) -> list:
        return self._boolean_vector

    @vector.setter
    def vector(self, vec) -> None:
        """
        Свойство, которое проверяет длину вектора (вектор всегда кратен 2), проверяет значения
        """
        if len(vec) % 2 != 0 or len(vec) % 6 == 0:
            raise ValueError("Ввели неправильный вектор по длине ")
        if not all(map(lambda x: 0 <= x <= 1, vec)):
            raise ValueError("Функция может содержать только 0 и 1")
        self._boolean_vector = vec

    @counter
    def __xor_elements(self, vector) -> list:
        """
        Метод, который проводит xor попарно между элементами
        """
        print(f"{self.__xor_elements.count} строка треугольника -  {' '.join(map(str, vector)):^20}")
        vector = [x ^ y for x, y in pairwise(vector)]
        return vector

    def get_polynom_triangle(self) -> list:
        """
        Здесь мы получаем коэффициенты для конечной записи полинома Жегалкина
        """
        result = [self._boolean_vector[0]]
        vector = self._boolean_vector.copy()
        while len(current_row := self.__xor_elements(vector)) > 0:
            result.append(current_row[0])
            vector = current_row
        return result

    def make_polynom_fft(self):
        first_raw = self._boolean_vector.copy()
        counter_raw = 1
        while counter_raw != int(log2(len(first_raw))) + 1:
            print(list(self.chunked(first_raw, counter_raw * 2)))
            counter_raw += 1

    def print_res(self) -> None:
        table = PrettyTable()
        table.field_names = ("x", "y", "z", "f")
        table.add_rows(
            np.insert(self.table, len(self.table[0]), np.array(self._boolean_vector),
                      axis=1))
        print("Все булевы строки матрицы: ", table, sep='\n')
        res = ""
        for value, raw in zip(self.get_polynom_triangle(), self.table):
            if value == 1:
                res += "1" * np.array_equal(raw, np.zeros(3)) + " ⊕ " + ''.join(compress(("x", "y", "z"), raw))
        print(f"Результат полинома Жегалкина - {res.strip(' ⊕ ')}")

        self.make_polynom_fft()

    @staticmethod
    def chunked(iterable, n):
        """
        Разбивает итерируемую последовательность на группы размером n.
        """
        it = iter(iterable)
        while True:
            chunk = list(islice(it, n))
            if not chunk:
                return
            yield chunk


def main() -> None:
    try:
        s = list(map(int, input("Введите функцию - вектор для Полинома Жегалкина ").split()))
        result = Polynom(s)
        result.print_res()
    except ValueError:
        raise ValueError("Вы использовали не целые числа при записи")


if __name__ == "__main__":
    main()
