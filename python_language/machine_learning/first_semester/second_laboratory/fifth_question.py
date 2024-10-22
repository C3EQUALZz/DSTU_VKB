"""
Задан список с числами.
Напишите функцию, которая меняет местами наибольший и наименьший элемент и возвращает новый список.
"""


def change_max_min(numbers: list[int]) -> list[int]:
    result = numbers.copy()
    i, j = numbers.index(max(numbers)), numbers.index(min(numbers))
    result[i], result[j] = result[j], result[i]
    return result


def main() -> None:
    user_input = input("Вводите числа через пробел: ").strip().split()

    if all(x.isdigit() or (x[0] == "-" and x[1:].isdigit()) for x in user_input):
        print(change_max_min(list(map(int, user_input))))
    else:
        print("Вы ввели не числа")


if __name__ == '__main__':
    main()
