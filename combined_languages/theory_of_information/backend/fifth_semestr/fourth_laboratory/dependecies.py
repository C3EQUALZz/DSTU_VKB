"""
Лабораторная работа 4

Здесь я не нашел готовых реализаций в Интернете, поэтому писал сам все вручную.
Не совсем идеальная архитектура, не придумал как лучше на данный момент.

Тестовые данные

matrix = [
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 1],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 1]
    ]

execute(
    "Огромное сообщение",
    matrix,
    'G'
)

matrix = [
    [1, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1]
]

execute(
    "Как дела?",
    matrix,
    "H"
)
"""
from typing import AnyStr, Literal, List, Mapping, Union

import numpy as np

from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.code_table import \
    find_errors
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.models.table_of_error_vectors_and_syndromes import \
    create_table_of_error_vectors_and_syndromes
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.helpers import \
    get_info_for_encoding, get_verification_systematic_transposed_matrix
from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.registry import Registry


def generate_errors(
        word: AnyStr,
        n: int
) -> AnyStr:
    """
    Здесь происходит имитация канала передачи информации.

    В каждую последовательность длиной n (в каждое кодовое слово) добавляется на случайную позицию одна ошибка
    (0 меняется на 1, 1 на 0).
    Отдельно каждый такой блок назовем v.

    :param word: Набор битов, в которое мы хотим внести ошибки.
    :param n: Длина, через которую мы хотим вводить ошибки.
    :returns: Возвращает видоизмененную строку после канала
    """
    array = np.array([int(x) for x in word])
    array[::n] = np.logical_not(array[::n])
    return "".join(map(str, array))


def encode(
        word: AnyStr,
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"]
) -> AnyStr:
    """
    Здесь происходит вся логика кодирования сообщения (ТОЛЬКО КОДИРОВАНИЕ, БЕЗ КАНАЛА).

    :param word: Слово, которое хочет закодировать пользователь.
    :param matrix: H (проверочная) или G (порождающая) матрица.
    :param type_matrix: Тип матрицы (H или G).
    :returns: Закодированную строку.
    """
    # Я не знаю как избежать нечетной длины символов, так как если k = 3 и т.п, то просто все ломается
    # Единственный вариант решения - это добавить пробел, тогда все работает идеально.
    if len(word) % 2 == 1:
        word += " "

    code_table, generation_sys_matrix = get_info_for_encoding(matrix, type_matrix)
    binary_word = ''.join(format(x, '08b') for x in bytearray(word, 'utf-8'))
    count_of_rows = len(generation_sys_matrix)
    blocks = [list(map(int, binary_word[i:i + count_of_rows])) for i in
              range(0, len(binary_word), count_of_rows)]

    encoded_word = []

    for block in blocks:
        # Находим индекс блока в столбце информационных слов
        index = np.where((code_table.information_words_column == block).all(axis=1))[0][0]
        # Получаем соответствующее значение из столбца кодовых слов
        encoded_block = code_table.code_words_column[index]
        encoded_word.extend(encoded_block)

    _ = find_errors(code_table)

    return "".join(map(str, encoded_word))


def decode(
        encoded_with_errors: AnyStr,
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"]
) -> AnyStr:
    """
    Функция для декодирования потока байтов после добавок ошибок из канала.
    :param encoded_with_errors: Поток байтов, пришедший после канала сообщений.
    :param matrix: Матрица, которая пользовалась при кодировании (вручную пользователь вводил).
    :param type_matrix: Тип матрицы, который ввел пользователь (G или H).
    :returns: Декодированное слово в utf-8. Задумано получить то же самое, что ввел пользователь.
    """
    code_table, generation_sys_matrix = get_info_for_encoding(matrix, type_matrix)
    verification_systematic_matrix_transposed = get_verification_systematic_transposed_matrix(matrix, type_matrix)
    table = create_table_of_error_vectors_and_syndromes(verification_systematic_matrix_transposed)
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

    binary_word = "".join(map(str, decoded_binary_word))

    byte_chunks = [binary_word[i:i + 8] for i in range(0, len(binary_word), 8)]

    byte_array = bytearray(int(byte, 2) for byte in byte_chunks)

    return ''.join(char for char in byte_array.decode('utf-8') if char.isprintable())


def execute(
        word: AnyStr,
        matrix: List[List[int]],
        type_matrix: Literal["G", "H"]
) -> Mapping[AnyStr, Union[List[List[int]], int]]:
    """
    Запуск всех шагов по выполнению лабораторной работы.
    - Кодирование
    - Канал с ошибками
    - Декодирование

    :param word: Слово, которое ввел пользователь для кодирования.
    :param matrix: Матрица, введенная пользователем для выполнения алгоритма.
    :param type_matrix: Тип матрицы (G или H)
    :returns: Словарь с данными на frontend
    """
    Registry.clear()

    encoded_word = encode(word, matrix, type_matrix)
    encoded_word_with_errors = generate_errors(encoded_word, len(matrix[0]))
    _ = decode(encoded_word_with_errors, matrix, type_matrix)

    return Registry().get_all_info()
