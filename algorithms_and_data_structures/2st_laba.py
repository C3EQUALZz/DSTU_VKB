"""
Все лабы были реализованы на 1 курсе, когда плохо знал Python, много неправильных записей и опечаток, но рабочее все.
Переделывать нет времени.
"""
import random, copy, numpy as np

n, m = map(int, input('Введите два числа размерности матрицы: ').split())
matrix = np.array([[random.randint(-1000, 1000) for x in range(m)] for _ in range(n)])
mas = np.array(copy.deepcopy(matrix))
lst = [int(x) for x in input('Вводите числа: ').split()]
search_value = int(input('Введите число для бинарного поиска: '))
enter = '\n'


# 1 задание

def quick_sort(matrix):
    if len(matrix) > 1:
        x = matrix[random.randint(0, len(matrix) - 1)]
        low = [l for l in matrix if l < x]
        eq = [l for l in matrix if l == x]
        high = [l for l in matrix if l > x]
    return quick_sort(low) + eq + quick_sort(high)


def matrix_sort(mas):
    for k in range(m):
        mas[:, k] = quick_sort(matrix[:, k])
    return print(f'Изначальный массив: {enter} {np.around(matrix, decimals=3)}',
                 f'После сортировки массив: {enter} {np.around(mas, decimals=3)}', sep='\n')


# 2 задание

def merge_list(a, b):
    sum_list, c = a + b, []
    while sum_list:
        c.append(sum_list.pop(sum_list.index(min(sum_list))))
    return c


def split_and_merge_list(lst):
    a, b = lst[len(lst) // 2:], lst[:len(lst) // 2]
    if len(a) > 1:
        a = split_and_merge_list(a)
    if len(b) > 1:
        b = split_and_merge_list(b)

    return merge_list(a, b)


# 3 задание

search_list = split_and_merge_list(lst)


def binary_search(search_list, search_value):
    spisok = search_list
    high, low, middle = len(spisok) - 1, 0, 0

    while low <= high and middle != search_value:
        middle = (low + high) // 2
        guess = spisok[middle]
        if guess == search_value:
            return middle
        elif guess > search_value:
            high = middle - 1
        else:
            low = middle + 1
    else:
        return 'Элемент в массиве не найден'


if __name__ == '__main__':
    print(f'Результат после сортировки: {split_and_merge_list(lst)}')
    print(f'Результат бинарного поиска: {binary_search(search_list, search_value)}')
    print(matrix_sort(mas))
