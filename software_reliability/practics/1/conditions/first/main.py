"""
Написать и протестировать функцию, которая "переворачивает" строку, передаваемую в качестве параметра, в зеркальное состояние
"""
from io import StringIO
from typing import AnyStr, List


def reverse(string: AnyStr) -> AnyStr:
    """
    Функция, которая разворачивает строку.

    Здесь сделан слишком сильный императивный код, чтобы radon мог анализировать нормально.
    В случае использования по типу str(reversed(string)) просто все метрики будут по 0.

    Args:
        string: любая строка
    Returns:
        Развернутую строку.
    """
    list_with_alphas: List[AnyStr] = list(string)
    buffer: StringIO = StringIO()

    middle_index: int = len(string) // 2
    index: int = 0

    while index != middle_index:
        list_with_alphas[index], list_with_alphas[~index] = list_with_alphas[~index], list_with_alphas[index]
        index += 1

    for alpha in list_with_alphas:
        buffer.write(str(alpha))

    reversed_string: str = buffer.getvalue()

    buffer.close()

    return reversed_string


def main() -> None:
    while True:
        s: str = input("Введите строку для разворота")
        print(reverse(s))

if __name__ == "__main__":
    main()
