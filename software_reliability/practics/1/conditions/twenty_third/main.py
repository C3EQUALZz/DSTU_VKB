"""
Вариант 23. Написать и протестировать функцию, которая в строке, передаваемой ей в качестве параметра,
заменяет каждый второй элемент на заданный символ.
"""
from typing import List


def replace_second_chars(s: str, char: str) -> str:
    """
    Заменяет каждый второй элемент строки на указанный символ.

    Аргументы:
        s (str): Исходная строка.
        char (str): Символ для замены.

    Возвращает:
        str: Модифицированная строка.

    Вызывает:
        ValueError: Если char не является одним символом.
    """
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("char должен быть одним символом.")

    # Преобразуем строку в список для изменения элементов
    s_list: List[str] = list(s)

    # Заменяем каждый второй символ (индексы 1, 3, 5...)
    for i in range(1, len(s), 2):
        s_list[i] = char

    return ''.join(s_list)


def main() -> None:
    """
    Основная функция, запрашивающая ввод и выводящая результат.
    """
    try:
        user_input = input("Введите строку: ")
        replacement_char = input("Введите символ для замены: ")

        if len(replacement_char) != 1:
            raise ValueError("Символ замены должен быть ровно одним символом.")

        result = replace_second_chars(user_input, replacement_char)
        print("Результат:", result)

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
