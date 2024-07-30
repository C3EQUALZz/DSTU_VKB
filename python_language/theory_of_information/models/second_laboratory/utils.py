from typing import List
from python_language.theory_of_information.models.second_laboratory import Token
from prettytable import PrettyTable


def create_table(tokens: List[Token], text: str) -> PrettyTable:
    search_buffer = [""] * 9
    lookahead_buffer = list(text[:7])
    decoded_string = ""
    table = PrettyTable()
    table.field_names = ["Словарь", "Буфер", "Код"]

    for token in tokens:
        search_buffer, lookahead_buffer, decoded_string, text = update_buffers(token, search_buffer, lookahead_buffer,
                                                                               decoded_string, text)
        search_str = "".join(search_buffer).ljust(9)
        lookahead_str = "".join(lookahead_buffer).ljust(7)
        code_str = f"<{token.offset},{token.length},{token.indicator}>"
        table.add_row([search_str, lookahead_str, code_str])

    return table


def update_buffers(token, search_buffer, lookahead_buffer, decoded_string, text):
    offset, length, char = token
    start = len(decoded_string) - offset if offset != 0 else 0
    match = decoded_string[start:start + length]
    sequence = match + char
    decoded_string += sequence
    search_buffer = list(decoded_string[-9:])
    remaining_text = text[len(sequence):]
    lookahead_buffer = list(remaining_text[:7])
    return search_buffer, lookahead_buffer, decoded_string, remaining_text
