"""
Дополните код из предыдущего задания, чтобы теперь получилась пирамида.
То есть каждая ступень состоит из чисел от 1 до i и обратно.
"""


def ladder(size: int) -> list[str]:
    result: list[str] = []

    for i in range(1, size + 1):
        ascending_part = ''.join(str(x) for x in range(1, i + 1))
        descending_part = ''.join(str(x) for x in range(i - 1, 0, -1))
        spaces = ' ' * (size - i)
        result.append(spaces + ascending_part + descending_part)

    return result


def main() -> None:
    user_input = input("Введите положительное число - количество строк пирамиды: ")

    if user_input.isdigit():
        print("\n".join(ladder(int(user_input))))
    else:
        print("Вы ввели не число")


if __name__ == '__main__':
    main()
