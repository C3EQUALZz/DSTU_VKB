from combined_languages.theory_of_information.backend.fifth_semestr.fourth_laboratory.utils.helpers import \
    create_table_for_encoding
import numpy as np


def execute(word: str, matrix: list[list[int]], type_matrix: str) -> str:
    code_table = create_table_for_encoding(matrix, type_matrix)
    binary_word = ''.join(format(x, 'b') for x in bytearray(word, 'utf-8'))
    blocks = [list(map(int, binary_word[i:i + len(matrix)])) for i in range(0, len(binary_word), len(matrix))]

    encoded_word = []
    for block in blocks:
        # Находим индекс блока в столбце информационных слов
        index = np.where((code_table.information_words_column == block).all(axis=1))[0][0]
        # Получаем соответствующее значение из столбца кодовых слов
        encoded_block = code_table.code_words_column[index]
        encoded_word.extend(encoded_block)


    return "".join(map(str, encoded_word))


if __name__ == '__main__':
    matrix = [
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 1],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 1]
    ]

    execute(
        "Привет",
        matrix,
        'G'
    )
