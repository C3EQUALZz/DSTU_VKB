from python_language.theory_of_information.models.second_laboratory import Token
from prettytable import PrettyTable
from typing import Final

SEARCH_BUFFER_SIZE: Final = 9
LOOK_AHEAD_SIZE: Final = 7


def create_table(tokens: list[Token], text: str) -> PrettyTable:
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
        search_buffer, lookahead_buffer, decoded_string, text = update_buffers(token, decoded_string, text)
        search_str = "".join(search_buffer).ljust(SEARCH_BUFFER_SIZE)
        lookahead_str = "".join(lookahead_buffer).ljust(LOOK_AHEAD_SIZE)
        code_str = f"<{token.offset},{token.length},{token.indicator}>"
        table.add_row([search_str, lookahead_str, code_str])

    return table


def update_buffers(
        token: Token,
        decoded_string: str,
        text: str
) -> tuple[list[str], list[str], str, str]:
    """
    Обновите буферы поиска и предварительного просмотра после обработки токена.

    :param token: The current token being processed.
    :param decoded_string: The decoded string so far.
    :param text: Remaining text to encode.
    :return: Updated search buffer, lookahead buffer, decoded string, and remaining text.
    """
    offset, length, char = token
    start = len(decoded_string) - offset if offset != 0 else 0
    sequence = decoded_string[start:start + length] + char
    decoded_string += sequence
    search_buffer = list(decoded_string[-SEARCH_BUFFER_SIZE:])
    remaining_text = text[len(sequence):]
    lookahead_buffer = list(remaining_text[:LOOK_AHEAD_SIZE])
    return search_buffer, lookahead_buffer, decoded_string, remaining_text
