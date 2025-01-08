"""
Задача №1327. Период строки

Дана непустая строка s. Нужно найти такое наибольшее число k и строку t, что s совпадает со строкой t, выписанной k раз подряд.

Ограничение времени - 1 секунда.

Входные данные

Одна строка длины N, 0 < N ≤ 106, состоящая только из маленьких латинских букв.

Выходные данные

Одно число - наибольшее возможное k.
"""


def find_max_repetition_count(s: str) -> int:
    length = len(s)
    for period_length in range(1, length // 2 + 1):
        if length % period_length == 0 and s[:period_length] * (length // period_length) == s:
            return length // period_length
    return 1

def main() -> None:
    input_string = input().strip()

    print(find_max_repetition_count(input_string))

if __name__ == '__main__':
    main()
