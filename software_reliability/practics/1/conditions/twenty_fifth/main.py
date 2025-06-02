"""
Вариант 25. Написать и протестировать функцию, которая преобразует строку шестнадцатеричных элементов числа в
эквивалентное ей целое десятичное число.
"""


def hex_to_decimal(hex_str: str) -> int:
    """
    Преобразует шестнадцатеричную строку в десятичное число.

    Аргументы:
        hex_str (str): Строка, представляющая шестнадцатеричное число (0-9, A-F, a-f).

    Возвращает:
        int: Десятичное представление шестнадцатеричного числа.

    Вызывает:
        ValueError: Если строка содержит недопустимые символы или пуста.
    """
    if not hex_str:
        raise ValueError("Входная строка не может быть пустой.")

    hex_digits: str = "0123456789ABCDEF"
    hex_str: str = hex_str.upper()

    decimal: int = 0
    for char in hex_str:
        if char not in hex_digits:
            raise ValueError(f"Недопустимый символ: '{char}'. Допустимые символы: 0-9, A-F.")
        decimal: int = decimal * 16 + hex_digits.index(char)

    return decimal


def main() -> None:
    """
    Основная функция, запрашивающая ввод и выводящая результат.
    """
    try:
        user_input: str = input("Введите шестнадцатеричное число: ").strip()
        decimal_number = hex_to_decimal(user_input)
        print(f"Десятичное число: {decimal_number}")

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
