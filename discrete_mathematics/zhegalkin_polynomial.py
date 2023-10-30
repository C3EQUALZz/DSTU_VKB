"""
Выполнил Ковалев Данил ВКБ22
Лабораторная 2
"""
from itertools import pairwise, product
import numpy as np


class Polynom:
    def __init__(self, vector: list):
        self.vector = vector
        self.result = [self._vector[0]]
        self.table = self.create_table()
        print(self.table)

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, vec):
        if len(vec) % 2 != 0:
            raise ValueError("Ввели неправильный вектор по длине ")
        if not all(map(lambda x: 0 <= x <= 1, vec)):
            raise ValueError("Функция может содержать только 0 и 1")
        self._vector = vec

    def get_polynom_triangle(self):
        while len(current_row := self.__xor_elements()) > 0:
            self.result.append(current_row[0])
        return self.result

    def __xor_elements(self):
        print(f"Текущая строка треугольника - {self._vector}")
        self._vector = [x ^ y for x, y in pairwise(self._vector)]
        return self._vector

    @staticmethod
    def create_table() -> np._typing.NDArray:
        return np.array([list(x) for x in product([0, 1], repeat=3)]).transpose()


def main():
    s = list(map(int, input("Введите функцию - вектор для Полинома Жегалкина ").split()))
    result = Polynom(s)
    print(f"Результат полинома Жегалкина - {' xor '.join(map(str, result.get_polynom_triangle()))}")


if __name__ == "__main__":
    main()

# 0 1 1 1 0 0 1 1
