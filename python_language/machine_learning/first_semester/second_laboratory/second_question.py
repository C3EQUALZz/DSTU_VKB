"""
По-данному натуральному n <= 9 выведите лесенку из n ступенек, i-я ступенька состоит из чисел от 1 до i без пробелов.

---
Входные данные: 1

Выходные данные:
1
---
Входные данные: 3

Выходные данные:
1
12
123
---
Входные данные: 5

Выходные данные:
1
12
123
1234
12345
"""


def ladder(number: int) -> str:
    result: list[str] = []

    for row in range(1, number + 1):
        buffer = ""
        for current_number in range(1, row + 1):
            buffer += str(current_number)

        if buffer:
            result.append(buffer)

    return "\n".join(result)


def main() -> None:
    if (user_input := input("Введите положительное число - количество строк лестницы: ")).isdigit():
        print(ladder(int(user_input)))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
