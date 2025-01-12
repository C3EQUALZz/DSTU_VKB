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
from typing import Final, Dict, List, Sequence, AnyStr

BRACKET_PAIRS: Final[Dict[str, str]] = {
    '(': ')',
    '[': ']',
    '{': '}'
}


def reconstruct(
        s: AnyStr,
        distance_table: Sequence[Sequence[int]],
        table_for_restoring_sequence: Sequence[Sequence[int]],
        l: int,
        r: int
) -> AnyStr:
    """
    Восстанавливает правильную последовательность из таблиц.

    Алгоритм работы:
    1. Проверяем, является ли подстрока s[l:r+1] уже правильной последовательностью:
       - Если distance_table[l][r] равно r - l + 1, это означает, что все символы уже в правильной последовательности.
         В этом случае возвращаем пустую строку, так как ничего удалять не нужно.
    2. Если distance_table[l][r] равно 0, это означает, что подстрока s[l:r+1] не может быть преобразована в правильную последовательность.
       В этом случае возвращаем всю подстроку s[l:r+1] как есть.
    3. Проверяем, есть ли индекс разделения для текущей подстроки:
       - Если table_for_restoring_sequence[l][r] равно -1, это означает, что нет разделения.
         В этом случае добавляем символ s[l] к результату, рекурсивно вызываем функцию для подстроки s[l+1:r-1] и добавляем символ s[r] в конец.
    4. Если есть индекс разделения, используем его для рекурсивного вызова функции:
       - Рекурсивно вызываем функцию для левой части подстроки s[l:split_index] и правой части s[split_index+1:r].
       - Объединяем результаты этих двух вызовов и возвращаем их как итоговую строку.

    :param s: Исходная строка, состоящая из скобок.
    :param distance_table: Таблица, где distance_table[l][r] хранит минимальное количество удалений для подстроки s[l:r+1].
    :param table_for_restoring_sequence: Таблица, где table_for_restoring_sequence[l][r] хранит индекс разделения
        для восстановления последовательности.
    :param l: Левый индекс текущей подстроки.
    :param r: Правый индекс текущей подстроки.
    """
    if distance_table[l][r] == r - l + 1:  # Все символы уже в правильной последовательности
        return ""
    if distance_table[l][r] == 0:  # Неправильная последовательность
        return s[l:r + 1]
    if table_for_restoring_sequence[l][r] == -1:  # Если нет разделения
        return s[l] + reconstruct(s, distance_table, table_for_restoring_sequence, l + 1, r - 1) + s[r]

    return (reconstruct(s, distance_table, table_for_restoring_sequence, l, table_for_restoring_sequence[l][r]) +
            reconstruct(s, distance_table, table_for_restoring_sequence, table_for_restoring_sequence[l][r] + 1, r))


def fill_tables(
        s: AnyStr,
        n: int,
        distance_table: List[List[int]],
        table_for_restoring_sequence: List[List[int]]
) -> None:
    """
    Заполняет таблицы для минимального количества удалений и восстановления последовательности.

    Алгоритм работы:
    1. Проходим по всем возможным правым индексам подстроки (right) от 0 до n-1.
    2. Для каждого правого индекса проходим по всем возможным левым индексам (left) от текущего правого индекса до 0.
    3. Если левый индекс равен правому (left == right), то это одиночный символ, который всегда требует 1 удаления.
    4. Если левый индекс меньше правого:
       a. Инициализируем переменные min_removals как бесконечность и split_index как -1.
       b. Проверяем, соответствует ли символы на позициях left и right (т.е. являются ли они парными скобками).
          - Если да, то обновляем min_removals значением из distance_table для подстроки между left и right.
       c. Разделяем подстроку на две части, перебирая все возможные разделительные индексы (k) между left и right.
          - Для каждого разделительного индекса вычисляем текущее количество удалений как сумму удалений для левой и правой подстрок.
          - Если текущее количество удалений меньше, чем min_removals, обновляем min_removals и split_index.
    5. После завершения всех проверок записываем минимальное количество удалений в distance_table[left][right] и
    индекс разделения в table_for_restoring_sequence[left][right].

    :param s: Исходная строка, состоящая из скобок.
    :param n: Длина строки s.
    :param distance_table: Таблица для хранения минимального количества удалений.
    :param table_for_restoring_sequence: Таблица для восстановления последовательности.
    :return: Ничего не возвращает, а только меняет текущий элемент. Сделано с той целью, чтобы не перегружать память.
    """
    for right in range(n):
        for left in range(right, -1, -1):
            if left == right:
                distance_table[left][right] = 1
            else:
                min_removals = float('inf')
                split_index = -1

                # Проверка на соответствие скобок
                if s[left] in BRACKET_PAIRS and s[right] == BRACKET_PAIRS[s[left]]:
                    min_removals = distance_table[left + 1][right - 1]

                # Разделение на подзадачи
                for k in range(left, right):
                    current_removals = distance_table[left][k] + distance_table[k + 1][right]
                    if min_removals > current_removals:
                        min_removals = current_removals
                        split_index = k

                distance_table[left][right] = min_removals
                table_for_restoring_sequence[left][right] = split_index


def min_removals_to_valid_parentheses(s: AnyStr) -> AnyStr:
    """
    Определяет наименьшее количество символов, которые необходимо удалить из строки,
    чтобы оставшиеся символы образовывали правильную скобочную последовательность.

    :param s: Исходная строка, состоящая из скобок.
    :returns: Строка максимальной длины, являющаяся правильной скобочной последовательностью.
    """

    n: int = len(s)
    # Один символ всегда является правильной последовательностью
    distance_table: List[List[int]] = [[1 if i == j else 0 for j in range(n)] for i in
                                       range(n)]  # Таблица для хранения минимального количества удалений
    table_for_restoring_sequence: List[List[int]] = [[0] * n for _ in
                                                     range(n)]  # Таблица для восстановления последовательности

    fill_tables(s, n, distance_table, table_for_restoring_sequence)

    return reconstruct(s, distance_table, table_for_restoring_sequence, 0, n - 1)


def main() -> None:
    s: str = input()
    result = min_removals_to_valid_parentheses(s)
    print(result)


if __name__ == "__main__":
    main()
