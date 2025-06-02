def octal_to_decimal(octal_str: str) -> int:
    """
    Преобразует строку, представляющую восьмеричное число, в целое десятичное число.

    Аргументы:
        octal_str (str): Строка, содержащая восьмеричные цифры (0-7).

    Возвращает:
        int: Десятичное представление восьмеричного числа.

    Вызывает:
        ValueError: Если строка содержит недопустимые символы или пуста.
    """
    if not octal_str:
        raise ValueError("Введенная строка пуста.")

    result: int = 0

    for char in octal_str:
        if not '0' <= char <= '7':
            raise ValueError(f"Недопустимый символ в строке: '{char}'")
        result: int = result * 8 + int(char)

    return result


def main() -> None:
    """
    Основная функция, запрашивающая ввод от пользователя и выводящая результат преобразования.
    """
    while True:
        user_input: str = input("Введите строку восьмеричных цифр: ")

        try:
            decimal_number: int = octal_to_decimal(user_input)
            print(f"Десятичное число: {decimal_number}")
        except ValueError as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
