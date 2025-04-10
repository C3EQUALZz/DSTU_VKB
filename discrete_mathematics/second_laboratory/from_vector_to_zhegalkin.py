from functools import wraps
from itertools import compress, islice, pairwise, product
from math import log2
from string import ascii_lowercase
from typing import Generator, Iterable, TypeAlias

import numpy as np
from prettytable import PrettyTable

Vector: TypeAlias = list[int, ...]


def counter(func):
    """
    Декоратор, который подсчитывает сколько раз мы вызвали функцию.
    Для вывода номера строки нужен
    """

    # сохранение __doc__ у декорируемой (функция, к которой применяется декоратор) функции
    @wraps(func)
    # наша вложенная функция, которая будет заменять декорируемую функцию
    def inner(*args, **kwargs):
        # атрибут count, который увеличивается каждый раз, когда мы вызываем декорируемую функцию
        inner.count += 1
        return func(*args, **kwargs)

    # изначально мы должны создать атрибут функции, чтобы дальше увеличивать счетчик
    inner.count = 0
    # возвращаем ссылку на нашу вложенную функцию, принцип построения декораторов
    return inner


class Polynom:
    """
    Главный класс, который реализует работу Полинома Жегалкина
    """

    def __init__(self, vector: Vector) -> None:
        """
        Args:
            vector (list): наша булева функция
        """
        self.vector: Vector = vector
        # Таблица вывода всех перестановок x, y, z. Ну там, где первая строчка "000", потом "001" и т.д
        self.table: np.ndarray = np.array(
            [np.array(x) for x in product([0, 1], repeat=int(log2(len(vector))))]
        )
        self.name_columns = tuple(ascii_lowercase[-int(log2(len(vector))) :])

    @property
    def vector(self) -> Vector:
        """
        Свойство, которое возвращает вектор. Свойства - более удачная альтернатива сеттерам, геттерам в Python
        """
        return self._boolean_vector

    @vector.setter
    def vector(self, vec: Vector) -> None:
        """
        Свойство, которое устанавливает значение для вектора нашего. То же свойство, но уже аналог сеттера.
        Args:
            vec (list[int, ...]): наш изначальный вектор, который мы ввели в консоль
        """
        # Длина вектора может быть только в виде 2**i
        if len(vec) % 2 != 0 or len(vec) % 6 == 0:
            raise ValueError(
                "Некорректная длина вектора функции, должно соблюдаться правило 2**n, где 0 <= n < float('inf')"
            )
        # Значения могут быть только 0 или 1 в векторах
        if not all(x == 0 or x == 1 for x in vec):
            raise ValueError(
                "Вектор функции может только содержать целые значения (0, 1)"
            )
        self._boolean_vector: Vector = vec

    @counter
    def __xor_elements(self, vector: Vector) -> Vector:
        """
        Метод, который попарно xor-ит элементы списка
        """
        # Вывод строки, здесь подсчет строки идет с помощью декоратора, каждый вызов увеличивает.
        # Во второй половине мы склеиваем наш вектор в строку и центрируем относительно 20 пустых ячеек (пробелов)
        print(
            f"{self.__xor_elements.count} строка треугольника -  {' '.join(map(str, vector)):^{len(self.vector) * 2}}"
        )
        # Пусть есть список [1,2,3], тогда pairwise([1,2,3]) -> iter((1,2), (2,3)).
        # Pairwise нужен, так как в треугольнике каждый соседний элемент надо xor-ить
        return [x ^ y for x, y in pairwise(vector)]

    def get_polynom_triangle(self) -> Vector:
        """
        Здесь мы получаем конечный вектор, который состоит из 1 первых элементов строки в треугольнике
        """
        # Сначала добавляем первый элемент из 1 строки
        result: Vector = [self.vector[0]]
        # Создаю копию, так как если сделать обычное присвоение мы полностью потеряем первоначальный вектор
        # В Python ссылочная модель, прочитайте в Интернете
        vector: Vector = self.vector.copy()
        # Цикл для реализации перехода к следующей строки треугольника. Ну как в ручном методе...
        # Здесь используется walrus operator, который присваивает, а потом возвращает значение
        while len(current_row := self.__xor_elements(vector)) > 0:
            # В результирующий вектор добавляю первый элемент каждой строки
            result.append(current_row[0])
            # Забываю про старую строку и присваиваем новую
            vector = current_row
        return result

    def __print_iter_res(self, argue: Vector) -> None:
        """
        Красивый вывод результата Полинома Жегалкина
        """
        # В начале проверяется с единицами. Потом мы просто сравниваем с переменными оставшимся.
        res: str = " ⊕ ".join(
            "1" * np.array_equal(raw, np.zeros(len(self.name_columns)))
            + "".join(compress(self.name_columns, raw))
            for value, raw in zip(argue, self.table)
            if value == 1
        )
        print(f"Результат полинома Жегалкина - {res}")

    def __print_table(self) -> None:
        """
        Красивый вывод таблицы
        """
        table: PrettyTable = PrettyTable()
        table.field_names = self.name_columns + ("f",)
        table.add_rows(
            np.insert(self.table, len(self.table[0]), np.array(self.vector), axis=1)
        )
        print("Все булевы строки матрицы: ", table, sep="\n")

    def print_res(self) -> None:
        """
        Сделал отдельный метод для единичного вызова печати класса
        """
        np.set_printoptions(threshold=np.inf)
        self.__print_table()
        self.__print_iter_res(self.get_polynom_triangle())
        res = self.make_fft_polynom()
        print(
            f"Матрица, которая была создана для преобразования Фурье \n {np.array(res)}"
        )
        self.__print_iter_res(res[-1])

    def make_fft_polynom(self) -> list[list[int, ...]]:
        """
        Не оптимизированная версия, но единственная, которую я смог придумать
        Реализация Полинома Жегалкина, используя БПФ
        https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BB%D0%B8%D0%BD%D0%BE%D0%BC_%D0%96%D0%B5%D0%B3%D0%B0%D0%BB%D0%BA%D0%B8%D0%BD%D0%B0
        """
        # Создаю матрицу
        matrix: list[list[int, ...]] = [self._boolean_vector]
        # Количество строк, то есть сколько раз мы повторим алгоритм
        for count_row in range(1, int(np.log2(len(self._boolean_vector))) + 1):
            # Временные контейнер данных и индекс
            result, counter_index = [], 0
            # Разбиваем, как на картинке в красные овалы
            for list_slice in self.chunked(matrix[count_row - 1], 2**count_row):
                # Проходимся поэлементно в нашем блоке красном
                for index, value in enumerate(list_slice):
                    # Если до половины красного блока, то добавляем.
                    # В ином случае элемент первой подгруппы (половина красного) с второй
                    result.append(
                        value
                        if index < len(list_slice) // 2
                        else matrix[count_row - 1][counter_index]
                        ^ matrix[count_row - 1][counter_index - len(list_slice) // 2]
                    )
                    counter_index += 1
            matrix.append(result)
        return matrix

    @staticmethod
    def chunked(iterable: Iterable, n: int) -> Generator[list, None, None]:
        """
        Разбивает итерируемую последовательность на группы размером n.
        На википедии - это красные прямоугольники
        """
        # Создаем итератор для оптимизации
        it: Iterable = iter(iterable)
        while True:
            # islice - аналог среза, который умеет работать с итераторами
            # Здесь проверка, что наш срез не пустой
            if not (chunk := list(islice(it, n))):
                return
            yield chunk
