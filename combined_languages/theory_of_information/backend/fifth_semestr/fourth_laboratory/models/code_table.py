from typing import TYPE_CHECKING
import itertools
import numpy as np
from dataclasses import dataclass

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
        GSystematicMatrix


@dataclass
class CodeTable:
    information_words_column: np.ndarray
    code_words_column: np.ndarray
    hamming_weights_column: np.ndarray

    def __iter__(self):
        return zip(self.information_words_column, self.code_words_column, self.hamming_weights_column)


@dataclass
class Errors:
    count_of_finds: int
    count_of_corrections: int


def create_code_table(generator_systematic_matrix: "GSystematicMatrix") -> CodeTable:
    """
    Генерирует кодовые слова и вычисляет веса Хэмминга для систематической матрицы G_s.

    :param generator_systematic_matrix: Систематическая матрица для построения кодовых слов.

    :returns: Массив, где каждая строка содержит кодовое слово и его вес Хэмминга.
    """
    # Генерация всех возможных информационных слов
    information_words_column = np.array(list(itertools.product([0, 1], repeat=generator_systematic_matrix.k)))

    # Генерация кодовых слов
    code_words_column = np.mod(information_words_column @ generator_systematic_matrix.matrix, 2)

    # Расчет веса Хэмминга для каждой строки
    hamming_weights_column = np.sum(code_words_column, axis=1)

    return CodeTable(information_words_column, code_words_column, hamming_weights_column)


def find_errors(table: CodeTable) -> Errors:
    """
    Поиск обнаруживающих ошибок и ошибок для исправления
    :param: таблица, которая состоит из информационных слов, кодовых слов и весов Хэмминга
    :returns: количество обнаружения ошибок и ошибок для исправления
    """
    d_min = np.min(table.hamming_weights_column > 0)
    finds = d_min - 1
    corr = (d_min - 1) / 2

    return Errors(finds, corr)
