# 1 вариант Ковалев Данил ВКБ22
from math import fabs


def first_question(a: float | int, b: float | int, c: float | int, k: float | int) -> None:
    try:
        print(fabs((a ** 2 / b ** 2 + c ** 2 * a ** 2) / (a + b + c * (k - a / b ** 3)) + c + (k / b - k / a) * c))
    except ZeroDivisionError:
        print("Деление на ноль")


def second_question(lst: list[str | int]) -> None:
    print(*lst[1::2], sep='\n') if isinstance(lst, list) else print("Вы ввели не список")


def third_question(lst: list[int]) -> None:
    print(sum(filter(lambda x: x > 10, map(int, lst))))


def last_question(lst):
    print(max(map(int, lst)))


def interact_with_user():
    match input("Какое задание вы хотите? Введите число от 1 до 4 "):
        case "1":
            first_question(*map(int, (input(f"Введите {letter} ") for letter in "abck")))
        case "2":
            second_question(eval(input("Введите список, как он выглядит в repr ")))
        case "3":
            third_question(eval(input("Введите список, как он выглядит в repr ")))
        case "4":
            last_question(eval(input("Введите список, как он выглядит в repr ")))
        case _:
            print("Вы выбрали неверный вариант")


if __name__ == "__main__":
    interact_with_user()
