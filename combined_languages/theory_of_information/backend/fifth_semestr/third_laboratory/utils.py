from typing import Final, overload

from prettytable import PrettyTable
from python_language.theory_of_information.models.second_laboratory import (
    TokenLZ77, TokenLZ78)

SEARCH_BUFFER_SIZE: Final = 9
LOOK_AHEAD_SIZE: Final = 7


@overload
def create_table(tokens: list[TokenLZ77], text: str) -> PrettyTable:
    """
    Создает таблицу, отображающую состояние процесса сжатия LZ77.

    :param tokens: Список токенов после сжатия LZ77.
    :param text: Оригинальный текст, который был сжат.
    :return: A PrettyTable, который выглядит, как в документе pdf
    """
    decoded_string = ""
    table = PrettyTable()
    table.field_names = ["Словарь", "Буфер", "Код"]

    for token in tokens:
        search_buffer, lookahead_buffer, decoded_string, text = update_buffers(
            token, decoded_string, text
        )
        search_str = "".join(search_buffer).ljust(SEARCH_BUFFER_SIZE)
        lookahead_str = "".join(lookahead_buffer).ljust(LOOK_AHEAD_SIZE)
        code_str = f"<{token.offset},{token.length},{token.indicator}>"
        table.add_row([search_str, lookahead_str, code_str])

    return table


def update_buffers(
    token: TokenLZ77, decoded_string: str, text: str
) -> tuple[list[str], list[str], str, str]:
    """
    Обновляем буфер поиска и предварительного просмотра после обработки токена.

    :param token: Токен, который нужно обработать.
    :param decoded_string: Декодированная строка, в которую мы добавляем токены.
    :param text: Текст, который мы собираемся дополнить.
    :return: Обновления.
    """
    start = max(0, len(decoded_string) - token.offset)
    sequence = decoded_string[start : start + token.length] + token.indicator
    decoded_string += sequence
    search_buffer = list(decoded_string[-SEARCH_BUFFER_SIZE:])
    remaining_text = text[len(sequence) :]
    lookahead_buffer = list(remaining_text[:LOOK_AHEAD_SIZE])
    return search_buffer, lookahead_buffer, decoded_string, remaining_text


def create_table(tokens: list[TokenLZ78], text: str) -> PrettyTable:
    table = PrettyTable()
    table.field_names = ["Входная фраза(в словарь)", "Код", "Позиция в словаре"]

    dictionary = {0: ""}
    position = 0

    for token in tokens:
        position += 1
        entry = dictionary.get(token.index, "") + token.char
        table.add_row([entry, repr(token), position])
        dictionary[position] = entry

    return table
