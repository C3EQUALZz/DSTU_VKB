from typing import TYPE_CHECKING, cast
import itertools
import numpy as np
from dataclasses import dataclass, asdict

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry

if TYPE_CHECKING:
    from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.generator_matrix import \
        GSystematicMatrix


@dataclass
class CodeTable:
    information_words_column: np.ndarray[np.ndarray[int]]
    code_words_column: np.ndarray[np.ndarray[int]]
    hamming_weights_column: np.ndarray[int]

    def __post_init__(self) -> None:
        data = asdict(self)

        for key, value in data.items():
            data[key] = value.tolist()

        Registry.log(f"Таблица информационных и кодовых слов {self.__class__.__name__}", data)

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
    info_words = np.array(list(itertools.product([0, 1], repeat=generator_systematic_matrix.k)))
    information_words_column = cast(np.ndarray[np.ndarray[int]], info_words)

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
    d_min = np.min(table.hamming_weights_column[table.hamming_weights_column > 0]).item()
    count_of_find_errors = d_min - 1
    count_of_corrections = int((d_min - 1) / 2)

    Registry.log("Минимальное расстояние Хэмминга", d_min)
    Registry.log("Количество обнаруживающих ошибок p", count_of_find_errors)
    Registry.log("Количество исправляющих ошибок", count_of_corrections)

    return Errors(count_of_find_errors, count_of_corrections)
