"""
Вариант 24. Написать и протестировать функцию для сложения и вычитания вещественных матриц.
Одним из формальных параметров должен быть признак вида операции.
"""

from typing import List, Union


def matrix_operation(
        a: List[List[Union[int, float]]],
        b: List[List[Union[int, float]]],
        operation: str
) -> List[List[Union[int, float]]]:
    """
    Выполняет сложение или вычитание матриц.

    Аргументы:
        a (List[List[Union[int, float]]]): Первая матрица.
        b (List[List[Union[int, float]]]): Вторая матрица.
        operation (str): Тип операции: 'add' или 'subtract'.

    Возвращает:
        List[List[Union[int, float]]]: Результирующая матрица.

    Вызывает:
        ValueError: Если матрицы не совместимы или операция неизвестна.
    """
    if not a or not b:
        raise ValueError("Матрицы не должны быть пустыми.")

    if len(a) != len(b):
        raise ValueError("Матрицы должны иметь одинаковое количество строк.")

    for row_a, row_b in zip(a, b):
        if len(row_a) != len(row_b):
            raise ValueError("Все строки матриц должны быть одинаковой длины.")

    if operation not in ("add", "subtract"):
        raise ValueError("Операция должна быть 'add' или 'subtract'.")

    result = []
    for row_a, row_b in zip(a, b):
        new_row = []
        for x, y in zip(row_a, row_b):
            if operation == "add":
                new_row.append(x + y)
            else:
                new_row.append(x - y)
        result.append(new_row)

    return result


def read_matrix(prompt: str) -> List[List[float]]:
    """
    Считывает матрицу от пользователя.

    Аргументы:
        prompt (str): Сообщение перед вводом матрицы.

    Возвращает:
        List[List[float]]: Считанная матрица.
    """
    print(prompt)
    rows: int = int(input("Количество строк: "))
    matrix: List[List[float]] = []
    for i in range(rows):
        row: List[float] = list(map(float, input(f"Строка {i + 1}: ").split()))
        matrix.append(row)
    return matrix


def main() -> None:
    """
    Основная функция, запрашивающая ввод и выводящая результат.
    """
    try:
        print("Первая матрица:")
        a: List[List[float]] = read_matrix("Первая матрица:")

        print("Вторая матрица:")
        b: List[List[float]] = read_matrix("Вторая матрица:")

        op: str = input("Введите операцию (add / subtract): ").strip().lower()
        result = matrix_operation(a, b, op)

        print("Результат:")
        for row in result:
            print(row)

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
