from typing import List, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
        GSystematicMatrix


class Matrix:
    def __init__(self, matrix: List[List[int]]) -> None:
        self.matrix = np.array(matrix)

    def transpose(self) -> "Matrix":
        return Matrix(self.matrix.transpose().tolist())

    @property
    def shape(self) -> tuple[int, ...]:
        return self.matrix.shape


class SystematicMatrix(Matrix):
    def __init__(self, matrix: List[List[int]]) -> None:
        super().__init__(matrix)

    def find_another_type_matrix(self) -> "SystematicMatrix":
        raise NotImplemented()

    @staticmethod
    def generate_code_table(generator_systematic_matrix: "GSystematicMatrix", k: int, n: int) -> np.ndarray:
        """
        Генерирует кодовые слова и вычисляет веса Хэмминга для систематической матрицы G_s.

        Параметры:
            G_s (np.ndarray): систематическая матрица для построения кодовых слов.
            k (int): количество информационных символов.
            n (int): общее количество символов в кодовом слове.

        Возвращает:
            np.ndarray: массив, где каждая строка содержит кодовое слово и его вес Хэмминга.
        """

        # Генерация всех возможных информационных слов
        t_i = np.zeros((1, k), dtype=int)
        for i in range(1, 2 ** k):
            bin_arr = bin(i)[2:].zfill(k)  # Двоичное представление с ведущими нулями
            t_i_new = [int(bit) for bit in bin_arr]
            t_i = np.vstack((t_i, t_i_new))

        # Генерация кодовых слов и расчет веса Хэмминга
        t_c = np.zeros((1, n), dtype=int)
        weights = []

        for i in range(1, 2 ** k):
            t_c_new = np.dot(t_i[i], generator_systematic_matrix.matrix) % 2  # Умножение на G_s и mod 2
            t_c = np.vstack((t_c, t_c_new))
            weights.append(np.sum(t_c_new))  # Вычисление веса Хэмминга для текущего кодового слова

        # Объединение информационных слов, кодовых слов и веса Хэмминга в единый массив
        weights = np.array(weights).reshape(-1, 1)
        code_table = np.hstack((t_i, t_c, weights))

        return code_table
