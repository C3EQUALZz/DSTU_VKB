"""
Дано натуральное число N. Вывести на экран число, которое получится после выписывания цифр числа N в обратном порядке.
Для получения нового числа составить функцию.
"""


def reverse_number(n: int) -> int:
    """
    Функция возвращает число, полученное обращением порядка цифр в заданном числе.

    Параметры:
        n (int): Исходное натуральное число

    Возвращает:
        int: Число с обратным порядком цифр
    """
    if not isinstance(n, int) or type(n) is bool:
        raise TypeError("По условию требуется число, а не всякое другое! ")

    if n < 1:
        raise ValueError("По условию требуется натуральное число")

    if 1 <= n <= 9:
        return n

    reversed_num: int = 0
    temp: int = n

    while temp > 0:
        last_digit = temp % 10
        reversed_num = reversed_num * 10 + last_digit
        temp //= 10

    return reversed_num


def main() -> None:
    """Основная функция для ввода данных и вывода результата"""
    while True:
        try:
            # Ввод числа с проверкой на натуральность
            n: int = int(input("Введите натуральное число N: "))

            if n < 0:
                print("Ошибка: Число должно быть натуральным (положительным)!")
                continue

            result: int = reverse_number(n)
            print(f"Число {n} в обратном порядке: {result}")

        except ValueError:
            print("Ошибка: Введите целое число!")


if __name__ == "__main__":
    main()
