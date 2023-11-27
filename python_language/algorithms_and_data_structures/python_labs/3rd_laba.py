# Вызов модулей
import copy, random, time, numpy as np

enter = '\n'


# Определение номера лабы и задания
def question(name):
    global zadanie
    if name == 1:
        print('Здесь есть только два задания: 1 - три вида сортировки, 2 - с помощью time сравнить данные сортировки')
        time.sleep(5)
        zadanie = int(input('Введите число номера задания данной лабораторной работы '))
    elif name == 2:
        print(
            'Здесь есть только три задания: 1 - сортировка Хоара по столбцам, 2 - сортировка слиянием на одномерном '
            'массиве, 3 - бинарный поиск')
        time.sleep(5)
        zadanie = int(input('Введите число номера задания данной лабораторной работы '))
    elif name == 3:
        print(
            'Здесь есть только два задания: 1 - объединить прошлые лабы, 2 - правильная последовательность с помощью '
            'стека, 3 - обратная польская запись')
        time.sleep(5)
        zadanie = int(input('Введите число номера задания данной лабораторной работы '))
    elif name == 0 or name > 3 or name < 0:
        print('Конец программы')
        exit()

    if (zadanie == 1 or zadanie == 2) and name == 1:  ##Вызов заданий для 1 лабы
        a = list(map(int, input('Вводите числа для одномерного массива ').split()))
        copy_a = copy.deepcopy(a)
        ccopy_a = copy.deepcopy(a)

        bubble_sort(a)
        choice_sort(copy_a)
        simple_insert(ccopy_a)

    if name == 2:
        if zadanie == 1:
            global matrix, m
            n, m = map(int, input('Введите два числа размерности матрицы: ').split())
            matrix = np.array([[random.randint(-1000, 1000) for x in range(m)] for _ in range(n)])
            mas = np.array(copy.deepcopy(matrix))

            formation_matrix(mas)

        elif zadanie == 2:
            lst = [int(x) for x in input('Вводите числа для сортировки слиянием: ').split()]

            print(f'Результат сортировки слиянием: {split_and_merge_list(lst)}')

        elif zadanie == 3:
            search_list = sorted([int(x) for x in input('Вводите числа для бинарного поиска: ').split()])
            print('Отсортированный список: ', *search_list)
            search_value = int(input('Введите число для бинарного поиска: '))

            binary_search(search_list, search_value)
    if name == 3:
        if zadanie == 2:
            raw_string = input('Введите скобочную последовательность: ')
            bracket_sequence(raw_string)
        elif zadanie == 3:
            raw_string = input('Введите польскую запись: ').split()
            polska_calculate(raw_string)


# Лаба 1, задание 1, 2
def bubble_sort(a):
    start = time.time()
    time.sleep(0.05)
    lst = copy.deepcopy(a)
    n = len(lst)
    for i in range(n - 1):
        flag = True
        for j in range(n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                flag = False
        if flag:
            break
    return print(f'Одномерный массив до сортировки : {a}', f'Одномерный массив после пузырьковой сортировки: {lst}',
                 sep='\n') \
        if zadanie == 1 else print(f'Время работы пузырьковой сортировки: {time.time() - start - 0.05}')


def choice_sort(copy_a):
    start = time.time()
    time.sleep(0.05)
    b = copy_a
    for k in range(len(b), 0, -1):
        b.append(b.pop(b.index(min(b[:k]))))
    return print(f'Одномерный массив до сортировки : {copy_a}', f'Одномерный массив после пузырьковой сортировки: {b}',
                 sep='\n') \
        if zadanie == 1 else print(f'Время работы пузырьковой сортировки: {time.time() - start - 0.05}')


def simple_insert(ccopy_a):
    start = time.time()
    lst = ccopy_a
    time.sleep(0.05)
    n = len(lst)
    for i in range(1, n):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j - 1], lst[j] = lst[j], lst[j - 1]
            else:
                break
    return print(f'Одномерный массив до сортировки : {ccopy_a}',
                 f'Одномерный массив после пузырьковой сортировки: {lst}', sep='\n') \
        if zadanie == 1 else print(f'Время работы соритровки вставкой: {time.time() - start - 0.05}')


# Лаба 2, задание 1

def quick_sort(matrix):
    if len(matrix) > 1:
        x = matrix[random.randint(0, len(matrix) - 1)]
        low = [l for l in matrix if l < x]
        eq = [l for l in matrix if l == x]
        high = [l for l in matrix if l > x]
    return quick_sort(low) + eq + quick_sort(high)


def formation_matrix(mas):
    for k in range(m):
        mas[:, k] = quick_sort(matrix[:, k])
        return print(f'Изначальный массив: {enter} {np.around(matrix, decimals=3)}'), \
            print(f'После сортировки массив: {enter} {np.around(mas, decimals=3)}')


# Лаба 2, задание 2

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


# Лаба 2, задание 3

def binary_search(search_list, search_value):
    spisok = search_list
    high, low, middle = len(spisok) - 1, 0, 0

    while low <= high and middle != search_value:
        middle = (low + high) // 2
        guess = spisok[middle]
        if guess == search_value:
            return print(f'Результат бинарного поиска по индексу: {middle}, а положение числа: {middle + 1}')
        elif guess > search_value:
            high = middle - 1
        else:
            low = middle + 1
    else:
        return 'Элемент в массиве не найден'


# Лаба 3, задание 2

def bracket_sequence(raw_string):
    stack, flag = [], True
    for i in raw_string:
        if i in ['(', '[', '{']:
            stack.append(i)
        elif i in [')', '}', ']']:
            if len(stack) == 0:
                flag = False
                break
            if (i == ')' and stack.pop() == '(') \
                    or (i == '}' and stack.pop() == '{') \
                    or (i == ']' and stack.pop() == '['):
                continue
            else:
                flag = False
                break
    return print('Является скобочной последовательностью') if flag == True else print(
        'Является не скобочной последовательностью')


# Лаба 3, задание 3

def polska_calculate(raw_string):
    stack = []
    flag = True
    for symbol in raw_string:
        if symbol.isdigit():
            stack.append(int(symbol))
        else:
            if len(stack) == 0:
                flag = False
                break
            if symbol == '*':
                stack.append(stack.pop() * stack.pop())
            elif symbol == '+':
                stack.append(stack.pop() + stack.pop())
            elif symbol == '-':
                i = stack.pop()
                j = stack.pop()
                stack.append(j - i)
            elif symbol == '/':
                i = stack.pop()
                j = stack.pop()
                stack.append(j / i)
    if flag:
        print(*stack)
    else:
        print('Ошибка')


while True:
    if __name__ == '__main__':
        name = int(input('Введи число для лабораторной работы: '))
        question(name)
