"""
Вариант 22. Написать и протестировать функцию, которая преобразует строку двоичных цифр
в эквивалентное ей целое десятичное число.
"""


def binary_to_decimal(binary_str: str) -> int:
    """
    Преобразует строку, представляющую двоичное число, в целое десятичное число.

    Аргументы:
        binary_str (str): Строка, содержащая только '0' и '1'.

    Возвращает:
        int: Десятичное представление двоичного числа.

    Вызывает:
        ValueError: Если строка содержит недопустимые символы или пуста.
    """
    if not binary_str:
        raise ValueError("Входная строка не может быть пустой.")

    decimal: int = 0
    for char in binary_str:
        if char not in ('0', '1'):
            raise ValueError(f"Недопустимый символ: '{char}'. Допустимые символы: '0' или '1'.")
        decimal: int = decimal * 2 + int(char)

    return decimal


def main() -> None:
    """
    Основная функция, запрашивающая ввод и выводящая результат.
    """
    try:
        user_input: str = input("Введите двоичное число: ")
        decimal_number: int = binary_to_decimal(user_input)
        print(f"Десятичное число: {decimal_number}")

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()