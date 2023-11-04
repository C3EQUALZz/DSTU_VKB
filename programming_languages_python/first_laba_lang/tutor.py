# 1 вариант Ковалев Данил ВКБ22
from math import fabs


def first_question(string: str) -> float | str:
    a, b, c, k = map(int, string.split())
    try:
        return fabs((a ** 2 / b ** 2 + c ** 2 * a ** 2) / (a + b + c * (k - a / b ** 3)) + c + (k / b - k / a) * c)
    except ZeroDivisionError:
        return "Деление на ноль"


def second_question(lst: list[str | int]) -> str:
    lst = eval(lst)
    return '\n'.join(str(x) for x in lst[1::2]) if isinstance(lst, list) else "Вы ввели не список"


def third_question(lst: list[int]) -> int:
    lst = eval(lst)
    return sum(filter(lambda x: x > 10, map(int, lst)))


def last_question(lst) -> int:
    lst = eval(lst)
    return max(map(int, lst))


def interact_with_user():
    match input("Какое задание вы хотите? Введите число от 1 до 4 "):
        case "1":
            print(first_question(*map(int, (input(f"Введите {letter} ") for letter in "abck"))))
        case "2":
            print(second_question(eval(input("Введите список, как он выглядит в repr "))))
        case "3":
            print(third_question(eval(input("Введите список, как он выглядит в repr "))))
        case "4":
            print(last_question(eval(input("Введите список, как он выглядит в repr "))))
        case _:
            print("Вы выбрали неверный вариант")


if __name__ == "__main__":
    interact_with_user()
