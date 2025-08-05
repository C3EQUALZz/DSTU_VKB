def octal_to_decimal(octal_str: str) -> int:
    return int(octal_str, 8)


def main() -> None:
    user_input: str = input("Введите строку восьмеричных цифр: ")
    decimal_number: int = octal_to_decimal(user_input)
    print(f"Десятичное число: {decimal_number}")


if __name__ == "__main__":
    main()
