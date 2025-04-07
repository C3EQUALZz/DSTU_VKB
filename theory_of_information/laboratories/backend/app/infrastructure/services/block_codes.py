import logging
from typing import Literal, cast, AnyStr, List

import numpy as np
from numpy.dtypes import StringDType

from app.domain.entities.block_codes.code_table import create_code_table, find_errors
from app.domain.entities.block_codes.factories.matrix import MatrixFactory
from app.domain.entities.block_codes.generator_systematic_matrix import GSystematicMatrix
from app.domain.entities.block_codes.table_of_error_vectors_and_syndromes import \
    create_table_of_error_vectors_and_syndromes
from app.domain.entities.block_codes.verification_systematic_matrix import HSystematicMatrix

logger = logging.getLogger(__name__)


class BlockCodesService:
    def encode(
            self,
            data: np.ndarray[tuple[str, str, str]],
            matrix: list[list[int]],
            type_matrix: Literal["G", "H"]
    ) -> str:
        """
        Здесь происходит вся логика кодирования сообщения (ТОЛЬКО КОДИРОВАНИЕ, БЕЗ КАНАЛА).

        :param data: Изображение в виде отображения массива пикселей, то есть [["11111111", "11111111", "11111111"], ["11111111", "11111111", "11111111"], ...]
        :param matrix: H (проверочная) или G (порождающая) матрица.
        :param type_matrix: Тип матрицы (H или G).
        :returns: Закодированную строку.
        """

        code_table, generation_sys_matrix = self.__get_info_for_encoding(matrix, type_matrix)
        binary_word = ''.join("".join(x) for x in data)

        count_of_rows = len(generation_sys_matrix)
        blocks = [list(map(int, binary_word[i:i + count_of_rows])) for i in range(0, len(binary_word), count_of_rows)]

        encoded_word = []

        for block in blocks:
            # Находим индекс блока в столбце информационных слов
            index = np.where((code_table.information_words_column == block).all(axis=1))[0][0]
            # Получаем соответствующее значение из столбца кодовых слов
            encoded_block = code_table.code_words_column[index]
            encoded_word.extend(encoded_block)

        return "".join(map(str, encoded_word))

    def decode(
            self,
            encoded_with_errors: AnyStr,
            matrix: List[List[int]],
            type_matrix: Literal["G", "H"]
    ) -> np.ndarray[list[str, str, str]]:
        """
        Функция для декодирования потока байтов после добавок ошибок из канала.
        :param encoded_with_errors: Поток байтов, пришедший после канала сообщений.
        :param matrix: Матрица, которая пользовалась при кодировании (вручную пользователь вводил).
        :param type_matrix: Тип матрицы, который ввел пользователь (G или H).
        :returns: Декодированное слово в utf-8. Задумано получить то же самое, что ввел пользователь.
        """
        code_table, generation_sys_matrix = self.__get_info_for_encoding(
            matrix,
            type_matrix
        )

        verification_systematic_matrix_transposed = self.__get_verification_systematic_transposed_matrix(
            matrix,
            type_matrix
        )

        table = create_table_of_error_vectors_and_syndromes(
            verification_systematic_matrix_transposed,
            find_errors(code_table)
        )

        count_columns = len(generation_sys_matrix[0])
        # Здесь создаем блоки v, как в методичке с размером k, где k - количество колонок.
        blocks = [list(map(int, encoded_with_errors[i:i + count_columns]))
                  for i in range(0, len(encoded_with_errors), count_columns)]

        decoded_binary_word = []

        for block in blocks:
            syndrome = np.dot(block, verification_systematic_matrix_transposed.matrix) % 2
            index = np.where((table.syndromes == syndrome).all(axis=1))[0][0]
            errors_block = table.errors[index]
            code_word = (errors_block + block) % 2

            index_of_code_word = np.where((code_table.code_words_column == code_word).all(axis=1))[0][0]
            decoded_block = code_table.information_words_column[index_of_code_word]
            decoded_binary_word.extend(decoded_block)

        binary_word: str = "".join(map(str, decoded_binary_word))

        byte_chunks = [binary_word[i:i + 8] for i in range(0, len(binary_word), 8)]

        result = cast(
            np.ndarray[list[str, str, str]],
            np.array([byte_chunks[i:i + 3] for i in range(0, len(byte_chunks), 3)], dtype=StringDType())
        )

        return result

    @staticmethod
    def __get_info_for_encoding(matrix: list[list[int]], type_matrix: Literal["G", "H"]):
        """
        Не совсем корректно делаю, что возвращаю в кортеже подобное. Неправильно построил архитектуру...
        В данной функции в начале создается с помощью фабрики матрица с нужным типом.
        После этого приводим к систематической форме и ищем обратную матрицу.
        Нам нужно в любом случае вернуть GSystematicMatrix, поэтому я на всякий случай инвертирую, а потом проверяю для возврата.
        :param matrix: Матрица, введенная пользователем.
        :param type_matrix: Тип матрицы H или G
        :returns: кортеж, состоящий из таблицы информационных и кодовых слов, а также систематическая матрица.
        """
        gen_or_check_matrix = MatrixFactory.create(matrix, type_matrix)
        gen_or_check_systematic_matrix = gen_or_check_matrix.to_systematic_form()
        inverse_systematic_matrix = gen_or_check_systematic_matrix.find_another_type_matrix()

        if inverse_systematic_matrix.__class__.__name__ == "GSystematicMatrix":
            matrix_for_table = cast(GSystematicMatrix, inverse_systematic_matrix)
        elif inverse_systematic_matrix.__class__.__name__ == "HSystematicMatrix":
            matrix_for_table = cast(GSystematicMatrix, gen_or_check_systematic_matrix)
        else:
            raise ValueError(f"Неправильный тип матрицы {inverse_systematic_matrix.__class__.__name__}")

        return create_code_table(matrix_for_table), matrix_for_table

    @staticmethod
    def __get_verification_systematic_transposed_matrix(
            matrix: List[List[int]],
            type_matrix: Literal["G", "H"]
    ) -> "HSystematicMatrix":
        """
        Получение Hsys^T матрицы из матрицы, введенной пользователем.
        Здесь в начале с помощью фабрики создается G или H матрица.
        После этого приводится в систематическую форму.
        :param matrix: Матрица, введенная пользователем.
        :param type_matrix: Порождающая (G) или проверочная (H) матрица.
        :returns: Проверочная систематическая матрица, которая была транспонирована (Hsys^T)
        """
        gen_or_check_matrix = MatrixFactory.create(matrix, type_matrix)
        gen_or_check_systematic_matrix = gen_or_check_matrix.to_systematic_form()
        inverse_systematic_matrix = gen_or_check_systematic_matrix.find_another_type_matrix()

        if inverse_systematic_matrix.__class__.__name__ == "HSystematicMatrix":
            result = cast(HSystematicMatrix, inverse_systematic_matrix.transpose())
        elif inverse_systematic_matrix.__class__.__name__ == "GSystematicMatrix":
            result = cast(HSystematicMatrix, gen_or_check_systematic_matrix.transpose())
        else:
            raise ValueError(f"Неправильный тип матрицы {inverse_systematic_matrix.__class__.__name__}")

        logger.info("Транспонированная проверочная систематическая матрица HSystematicMatrix %s",
                    result.matrix.tolist())

        return result
