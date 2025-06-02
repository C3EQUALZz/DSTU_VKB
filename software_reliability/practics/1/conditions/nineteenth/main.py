"""
Вариант 19. Выяснить, сколько простых чисел находится в интервале [n,m], и распечатать их.
Для определения, является ли очередное число простым, составить функцию.
"""

from typing import List


def is_prime(n: int) -> bool:
    """
    Проверяет, является ли число простым.

    Аргументы:
        n (int): Число для проверки.

    Возвращает:
        bool: True, если число простое, иначе False.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_primes_in_range(n: int, m: int) -> List[int]:
    """
    Возвращает список простых чисел в заданном диапазоне [n, m].

    Аргументы:
        n (int): Начало диапазона.
        m (int): Конец диапазона.

    Возвращает:
        List[int]: Список простых чисел.
    """
    if n > m:
        n, m = m, n
    return [num for num in range(n, m + 1) if is_prime(num)]


def main() -> None:
    """
    Основная функция, запрашивающая ввод и выводящая результат.
    """
    try:
        n: int = int(input("Введите начало диапазона n: "))
        m: int = int(input("Введите конец диапазона m: "))

        primes: List[int] = get_primes_in_range(n, m)

        print(f"Простые числа в диапазоне [{n}, {m}]:")
        print(primes)
        print(f"Количество простых чисел: {len(primes)}")

    except ValueError:
        print("Ошибка: Введите целые числа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
