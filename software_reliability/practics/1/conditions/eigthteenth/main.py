"""
Вариант 18. Составить и протестировать функцию для замены символов «:» на «.» в заданной строке, начиная с указанной позиции.
"""
from typing import List


def replace_colons(s: str, pos: int) -> str:
    """
    Заменяет все символы ':' на '.' в строке `s`, начиная с позиции `pos`.

    Аргументы:
        s (str): Исходная строка.
        pos (int): Позиция, с которой начинается замена.

    Возвращает:
        str: Строка с заменёнными символами.
    """
    if not s or pos >= len(s):
        return s

    if pos < 0:
        pos = 0

    # Замена символов
    s_list: List[str] = list(s)

    for i in range(pos, len(s)):
        if s_list[i] == ':':
            s_list[i] = '.'

    return ''.join(s_list)


def main() -> None:
    """
    Основная функция, запрашивающая ввод у пользователя и выводящая результат.
    """
    user_input: str = input("Введите строку: ")

    try:
        pos: int = int(input("Введите позицию для начала замены: "))
        result = replace_colons(user_input, pos)
        print("Результат:", result)
    except ValueError:
        print("Ошибка: Позиция должна быть целым числом.")


if __name__ == "__main__":
    main()
