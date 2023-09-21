# Все реализации сортировок
import random, heapq
import numpy as np
from numpy import *


def bubble_sort(lst: list) -> list:
    for i in range(len(lst) - 1):
        flag = True
        for j in range(len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                flag = False
        if flag == True:
            break
    return lst


def choice_sort(lst: list) -> list:
    for k in range(len(lst), 0, -1):
        lst.append(lst.pop(lst.index(min(lst[:k]))))
    return lst


def s_insert(lst: list) -> list:
    for i in range(1, len(lst)):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
            else:
                break
    return lst


def shell_sort(lst: list) -> list:
    move = len(lst) // 2
    while move > 0:
        for i in range(len(lst) - move):
            if lst[i] > lst[i + move]:
                lst[i], lst[i + move] = lst[i + move], lst[i]
        move //= 2
    return lst


def quick_sort(lst: list) -> list:
    if len(lst) > 1:
        x = lst[random.randint(0, len(lst) - 1)]
        low = [l for l in lst if l < x]
        eq = [l for l in lst if l == x]
        high = [l for l in lst if l > x]
        lst = quick_sort(low) + eq + quick_sort(high)
    return lst


def merge_sort(lst: list) -> list:
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

    return split_and_merge_list(lst)


def heap_sort(list_for_sort: list) -> list:
    heapq.heapify(list_for_sort)
    return [heapq.heappop(list_for_sort) for i in range(len(list_for_sort))]


def column_matrix_sort(mas):
    m = len(mas[1, :])
    for k in range(m):
        mas[:, k] = sorted(matrix[:, k])
        return np.around(mas, decimals=3)
