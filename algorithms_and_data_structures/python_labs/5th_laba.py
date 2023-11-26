import numpy as np
from algorithms_and_data_structures.python_labs.sorts import *
from algorithms_and_data_structures.python_labs.search import *
from algorithms_and_data_structures.python_labs.work_stats import *


def question():
    checker = lambda x: x.isdigit() if x[:1] != '-' else x[1:].isdigit()
    if input('Вы хотите посмотреть все виды сортировок? ') in ['Да', 'да', 'дА', 'ДА']:
        list_for_sort = [int(x) for x in input('Вводите числа для списка ').split() if checker(x)]

        print(f'Сортировка пузырьком {bubble_sort(list_for_sort)}')
        print(f'Сортировка выбором {choice_sort(list_for_sort)}')
        print(f'Сортировка вставкой {s_insert(list_for_sort)}')
        print(f'Сортировка Шелла {shell_sort(list_for_sort)}')
        print(f'Сортировка Хоара {quick_sort(list_for_sort)}')
        print(f'Сортировка слиянием {merge_sort(list_for_sort)}')
        print(f'Сортировка кучей {heap_sort(list_for_sort)}')

    elif input('Вы хотите сделать бинарный поиск? ') in ['Да', 'да', 'дА', 'ДА']:
        list_for_sort = [int(x) for x in input('Вводите числа для списка ').split() if checker(x)]

        try:
            search_value = int(input('Введите число, которое вы хотите искать '))
        except ValueError:
            if input('Вы ввели не int число. Заново') in ['Да', 'да', 'дА', 'ДА']:
                question()
            else:
                exit()

        print(f'Бинарный поиск {binary_search(list_for_sort, search_value)}')

    elif input('Вы хотите сортировать по столбцам матрицу? ') in ['Да', 'да', 'дА', 'ДА']:
        try:
            n = int(input('Введите количество строк матрицы '))
        except ValueError:
            if input('Вы ввели не int число. Заново? ') in ['Да', 'да', 'дА', 'ДА']:
                question()
            else:
                exit()

        matrix = np.array([[int(x) for x in input().split() if checker(x)] for i in range(n)])
        print(column_matrix_sort(matrix))

    elif input('Вы хотите посмотреть на задания, связанные со стеком? ') in ['Да', 'да', 'дА', 'ДА']:
        try:
            n = int(input('Введите, что выбрать. Польская запись или скобочная последовательность (1,2) '))
        except ValueError:
            if input('Вы ввели не int число. Заново? ') in ['Да', 'да', 'дА', 'ДА']:
                question()
            else:
                exit()
        if n == 1:
            raw_string = input('Введите скобочную последовательность: ')
            bracket_sequence(raw_string)
        elif n == 2:
            raw_string = input('Введите польскую запись: ').split()
            polska_calculate(raw_string)
        else:
            if input('Вы ввели неправильный номер. Заново? ') in ['Да', 'да', 'ДА', 'дА']:
                question()
            else:
                exit()

    elif input('Вы хотите начать работу с графом? ') in ['Да', 'да', 'ДА', 'дА']:
        if input('Вы хотите увидеть работу алгоритма поиска в глубину? ') in ['Да', 'да', 'ДА', 'дА']:
            try:
                start = int(input('С какой точки начать поиск в глубину у графа? '))
                end = int(input('В какую точку нужно прийти? '))
            except ValueError:
                if ('Вы ввели не число. Заново? ') in ['Да', 'да', 'ДА', 'дА']:
                    question()
                else:
                    exit()

            depth_first_search(start, end)

        elif input('Вы хотите увидеть работу алгоритма Дейкстры? ') in ['Да', 'да', 'ДА', 'дА']:
            try:
                start = int(input('С какой точки начать поиск в глубину у графа? '))
                end = int(input('В какую точку нужно прийти? '))
            except ValueError:
                if ('Вы ввели не число. Заново? ') in ['Да', 'да', 'ДА', 'дА']:
                    question()
                else:
                    exit()

            search_dejkstra(start, end)

        else:
            print('Вы ничего не выбрали')
            exit()


while True:
    if __name__ == '__main__':
        question()







