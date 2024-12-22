"""
Дополните код из предыдущего задания, чтобы теперь получилась пирамида.
То есть каждая ступень состоит из чисел от 1 до i и обратно.
"""


def ladder(size: int) -> str:
    result: list[str] = []

    for i in range(1, size + 1):
        spaces = " " * ((size * 2) - 2 * i)
        numbers = ' '.join(map(str, range(1, i + 1))) + ' ' + ' '.join(map(str, range(i - 1, 0, -1))) if i > 1 else '1'
        result.append(spaces + numbers)

    return "\n".join(result)


def main() -> None:
    user_input = input("Введите положительное число - количество строк пирамиды: ")

    if user_input.isdigit():
        print(ladder(int(user_input)))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
