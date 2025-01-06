"""
Задача №1905. Удаление скобок

Дана строка, составленная из круглых, квадратных и фигурных скобок.
Определите, какое наименьшее количество символов необходимо удалить из этой строки,
чтобы оставшиеся символы образовывали правильную скобочную последовательность.

Входные данные

Строка из круглых, квадратных и фигурных скобок. Длина строки не превосходит 100 символов.

Выходные данные

Выведите строку максимальной длины, являющуюся правильной скобочной последовательностью,
которую можно получить из исходной строки удалением некоторых символов.Если возможных ответов несколько, выведите любой из них.
"""


def min_removals_to_valid_parentheses(s: str) -> str:
    """Определяет наименьшее количество символов, которые необходимо удалить из строки,
    чтобы оставшиеся символы образовывали правильную скобочную последовательность."""

    n = len(s)
    dp = [[0] * n for _ in range(n)]  # Таблица для хранения минимального количества удалений
    pos = [[0] * n for _ in range(n)]  # Таблица для восстановления последовательности

    # Инициализация таблицы
    for i in range(n):
        dp[i][i] = 1  # Один символ всегда является правильной последовательностью

    # Заполнение таблицы
    for right in range(n):
        for left in range(right, -1, -1):
            if left == right:
                dp[left][right] = 1
            else:
                min_removals = float('inf')
                split_index = -1

                # Проверка на соответствие скобок
                if (s[left] == '(' and s[right] == ')') or \
                        (s[left] == '[' and s[right] == ']') or \
                        (s[left] == '{' and s[right] == '}'):
                    min_removals = dp[left + 1][right - 1]

                # Разделение на подзадачи
                for k in range(left, right):
                    current_removals = dp[left][k] + dp[k + 1][right]
                    if min_removals > current_removals:
                        min_removals = current_removals
                        split_index = k

                dp[left][right] = min_removals
                pos[left][right] = split_index

    # Восстановление правильной последовательности
    def reconstruct(l: int, r: int) -> str:
        if dp[l][r] == r - l + 1:  # Все символы уже в правильной последовательности
            return ""
        if dp[l][r] == 0:  # Неправильная последовательность
            return s[l:r + 1]
        if pos[l][r] == -1:  # Если нет разделения
            return s[l] + reconstruct(l + 1, r - 1) + s[r]

        return reconstruct(l, pos[l][r]) + reconstruct(pos[l][r] + 1, r)

    return reconstruct(0, n - 1)


def main() -> None:
    s = input()
    result = min_removals_to_valid_parentheses(s)
    print(result)


if __name__ == "__main__":
    main()
