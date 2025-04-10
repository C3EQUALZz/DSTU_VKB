"""
AUTHOR: 1 вариант Ковалев Данил ВКБ22
"""

import ast
from math import fabs


def safe_eval(expression: str):
    """
    Функция для безопасной работы с eval, потому что пользователь может так удалить папку или т.п важные папки
    """
    try:
        return ast.literal_eval(expression)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Произошла ошибка при обработке eval: {e}")


def first_question(string: str) -> float | str:
    """
    Напишите программу для решения примера. Есть переменные: a,b,c,k: Предусмотрите деление на 0.
    Все необходимые переменные вводите ниже.
    Пример ввода: 1 2 3 4
    """
    a, b, c, k = map(int, string.split())
    try:
        return fabs(
            (a**2 / b**2 + c**2 * a**2) / (a + b + c * (k - a / b**3))
            + c
            + (k / b - k / a) * c
        )
    except ZeroDivisionError:
        return "Деление на ноль"


def second_question(custom_string: str) -> str:
    """
    Дан произвольный список, содержащий и строки, и числа.
    Выведите все четные элементы построчно.
    Пример ввода: ["a", "b", 3, 5, 7, "aba"]
    """
    lst = safe_eval(custom_string)
    return (
        "\n".join(str(x) for x in lst[1::2])
        if isinstance(lst, list)
        else "Вы ввели не список"
    )


def third_question(custom_string: str) -> int:
    """
    Дан произвольный список, содержащий только числа.
    Выведите результат сложения чисел больше 10.
    Пример ввода: [1, 2, 3, 4, 15, 18, 20, -5]
    """
    return sum(filter(lambda x: x > 10, map(int, safe_eval(custom_string))))


def last_question(lst) -> int:
    """
    Дан произвольный список, содержащий только числа.
    Выведите максимальное число
    Пример ввода: [1, 2, 3, 4, 15, 18, 20, -5]
    """
    return max(map(int, safe_eval(lst)))


def interact_with_user():
    match input("Какое задание вы хотите? Введите число от 1 до 4 "):
        case "1":
            print(first_question(input(f"Введите a,b,c,k ")))
        case "2":
            print(second_question(input("Введите список, как он выглядит в repr ")))
        case "3":
            print(third_question(input("Введите список, как он выглядит в repr ")))
        case "4":
            print(last_question(input("Введите список, как он выглядит в repr ")))
        case _:
            print("Вы выбрали неверный вариант")


if __name__ == "__main__":
    interact_with_user()
