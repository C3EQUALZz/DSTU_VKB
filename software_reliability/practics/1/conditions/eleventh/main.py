"""
Вариант 11. Написать и протестировать функцию, которая подсчитывает,
сколько раз в заданной строке встретился указанный символ.
"""


def count_char(s: str, char: str) -> int:
    """
    Подсчитывает, сколько раз указанный символ встречается в строке.

    Аргументы:
        s (str): Исходная строка.
        char (str): Символ, количество вхождений которого нужно подсчитать.

    Возвращает:
        int: Количество вхождений символа в строку.

    Вызывает:
        ValueError: Если `char` не является одним символом.
    """
    if len(char) != 1:
        raise ValueError("Параметр 'char' должен быть ровно одним символом.")
    return s.count(char)


def main() -> None:
    """
    Основная функция, запрашивающая ввод у пользователя и выводящая результат.
    """
    try:
        user_string: str = input("Введите строку: ")
        user_char: str = input("Введите символ для поиска: ")

        if len(user_char) != 1:
            raise ValueError("Вы должны ввести ровно один символ.")

        result: int = count_char(user_string, user_char)
        print(f"Символ '{user_char}' встречается {result} раз(а).")

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()