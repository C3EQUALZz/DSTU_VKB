"""
Задача №1750. Подпалиндромы

Строка называется палиндромом, если она читается одинаково как слева направо, так и справа налево.
Например, строки abba, ata являются палиндромами.

Дана строчка. Ее подстрокой называется некоторая непустая последовательность подряд идущих символов.
Напишите программу, которая определит, сколько подстрок данной строки является палиндромами.

Входные данные

Вводится одна строка, состоящая из маленьких латинских букв. Длина строки не превышает 100000 символов.

Выходные данные

Выведите одно число — количество подстрок данной строки, являющихся палиндромами
"""


def find_palindromes(s: str) -> int:
    # Преобразуем строку для работы с палиндромами
    transformed_string = "@#" + "#".join(s) + "#$"
    palindrome_lengths = [0] * len(transformed_string)
    center = right_boundary = 0

    for i in range(1, len(transformed_string) - 1):
        if i < right_boundary:
            palindrome_lengths[i] = min(right_boundary - i, palindrome_lengths[2 * center - i])

        # Расширяем палиндром вокруг центра i
        while transformed_string[i + palindrome_lengths[i] + 1] == transformed_string[i - palindrome_lengths[i] - 1]:
            palindrome_lengths[i] += 1

        # Обновляем центр и правую границу, если нашли более длинный палиндром
        if i + palindrome_lengths[i] > right_boundary:
            center, right_boundary = i, i + palindrome_lengths[i]

    # Считаем количество палиндромных подстрок
    return sum((length + 1) // 2 for length in palindrome_lengths)


def main() -> None:
    input_string = input()
    print(find_palindromes(input_string))


if __name__ == "__main__":
    main()
