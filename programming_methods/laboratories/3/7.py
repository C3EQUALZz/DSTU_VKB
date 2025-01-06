"""
Задача №1124. Максимальный подпалиндром

Палиндромом называется строка, которая одинаково читается как слева направо, так и справа налево.
Подпалиндромом данной строки называется последовательность символов из данной строки, не обязательно идущих подряд,
являющаяся палиндромом.
Например, HELOLEH является подпалиндромом строки HTEOLFEOLEH.
Напишите программу, находящую в данной строке подпалиндром максимальной длины.

Входные данные

Во входном файле находится строка длиной не более 100 символов, состоящая из заглавных букв латинского алфавита.

Выходные данные

Выведите на первой строке выходного файла длину максимального подпалиндрома, а на второй строке сам максимальный
подпалиндром. Если таких подпалиндромов несколько, то ваша программа должна вывести любой из них.
"""

from typing import Tuple


def longest_palindromic_subsequence(s: str) -> Tuple[int, str]:
    n = len(s)
    # Таблица для хранения длины максимального подпалиндрома
    dp = [[0] * n for _ in range(n)]

    # Все одиночные символы являются палиндромами длины 1
    for i in range(n):
        dp[i][i] = 1

    # Заполнение таблицы
    for length in range(2, n + 1):  # Длина подстроки
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    # Длина максимального подпалиндрома
    max_length = dp[0][n - 1]

    # Восстановление самого подпалиндрома
    l, r = 0, n - 1
    subsequence = []

    while l <= r:
        if s[l] == s[r]:
            subsequence.append(s[l])
            l += 1
            r -= 1
        elif dp[l + 1][r] >= dp[l][r - 1]:
            l += 1
        else:
            r -= 1

    # Если длина подпалиндрома четная, то мы добавляем его в обратном порядке
    # Если нечетная, то добавляем последний символ
    palindromic_subsequence = ''.join(subsequence)
    if len(palindromic_subsequence) * 2 == max_length:
        result = palindromic_subsequence + palindromic_subsequence[::-1]
    else:
        result = palindromic_subsequence + palindromic_subsequence[-2::-1]

    return max_length, result


def main() -> None:
    s = input()
    max_length, palindromic_subsequence = longest_palindromic_subsequence(s)

    print(max_length)
    print(palindromic_subsequence)


if __name__ == "__main__":
    main()
