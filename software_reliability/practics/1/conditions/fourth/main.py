"""
Написать и протестировать функцию для вычисления числа сочетаний по формуле
"""

def combinations(n: int, k: int) -> int:
    """
    Вычисляет число сочетаний из n по k.

    Параметры:
        n (int): Общее количество элементов
        k (int): Количество выбираемых элементов

    Возвращает:
        int: Число сочетаний C(n, k)

    Исключения:
        ValueError: Если n или k отрицательные, либо k > n
    """
    if n < 0 or k < 0:
        raise ValueError("n и k должны быть неотрицательными")
    if k > n:
        return 0

    # Используем свойство симметрии C(n, k) = C(n, n-k)
    k: int = min(k, n - k)

    # Вычисляем по формуле: C(n, k) = ∏_{i=1}^{k} (n - i + 1) / i
    result: int = 1
    for i in range(1, k + 1):
        result *= (n - i + 1) // i

    return result


def main() -> None:
    """Основная функция для ввода данных и вывода результата"""
    print("Вычисление числа сочетаний C(n, k)")
    print("--------------------------------")

    # Ввод n с проверкой
    while True:
        try:
            n: int = int(input("Введите n (общее количество элементов): "))
            if n < 0:
                print("Ошибка: n должно быть неотрицательным!")
                continue
            break
        except ValueError:
            print("Ошибка: Введите целое число!")

    # Ввод k с проверкой
    while True:
        try:
            k: int = int(input("Введите k (количество выбираемых элементов): "))
            if k < 0:
                print("Ошибка: k должно быть неотрицательным!")
                continue
            break
        except ValueError:
            print("Ошибка: Введите целое число!")

    # Вычисление и вывод результата
    try:
        result = combinations(n, k)
        print(f"\nC({n}, {k}) = {result}")
    except ValueError as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()