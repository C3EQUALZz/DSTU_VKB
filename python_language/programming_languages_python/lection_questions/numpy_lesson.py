import numpy as np


def creating_numpy_arrays():
    # Создание numpy массива на основе списка
    a = np.array([1, 2, 3], dtype=np.uint8)

    # Создание array, которое содержит только 0
    b = np.zeros(3, dtype=np.int_)

    # Создание единичной матрицы
    c = np.eye(3, dtype=np.complex_)

    # Создание массива, содержащего случайные элементы
    d = np.empty((3, 3))

    # Создание последовательностей (старт, конец, шаг)
    e = np.arange(10, 100, 5)

    # Создание последовательностей (старт, конец, количество элементов)
    f = np.linspace(10, 100, 3)


def task():
    np.set_printoptions(precision=10, floatmode="fixed")
    x = np.linspace(-2 * np.pi, 2 * np.pi, 20)
    print((np.sin(x) ** 2 + np.cos(x) ** 2))
    print((np.sin(x) ** 2 + np.cos(x) ** 2) == 1)