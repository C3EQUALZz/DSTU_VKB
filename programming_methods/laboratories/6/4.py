"""
Задача №2782. Следующий

Реализуйте структуру данных, которая поддерживает множество S целых чисел, с котором разрешается производить следующие операции:

add(i) — добавить в множество S число i (если он там уже есть, то множество не меняется);
next(i) — вывести минимальный элемент множества, не меньший i.
Если искомый элемент в структуре отсутствует, необходимо вывести -1.

Входные данные

Исходно множество S пусто.
Первая строка входного файла содержит n — количество операций (1≤n≤300000).
Следующие n строк содержат операции.
Каждая операция имеет вид либо «+ i», либо «? i». Операция «? i» задает запрос next(i).

Если операция «+ i» идет во входном файле в начале или после другой операции «+», то она задает операцию add(i).
Если же она идет после запроса «?», и результат этого запроса был y, то выполняется операция add((i+y)mod10^9).

Во всех запросах и операциях добавления параметры лежат в интервале от 0 до 10^9.

Выходные данные

Для каждого запроса выведите одно число — ответ на запрос.

"""


import bisect

class SortedList:
    def __init__(self):
        self.list = []
        self.last_query = -1

    def add(self, x):
        if self.last_query != -1:
            x = (x + self.last_query) % 10**9
        pos = bisect.bisect_left(self.list, x)
        if pos == len(self.list) or self.list[pos] != x:
            bisect.insort(self.list, x)
        self.last_query = -1

    def next(self, x):
        pos = bisect.bisect_left(self.list, x)
        if pos < len(self.list):
            self.last_query = self.list[pos]
            return self.last_query
        else:
            self.last_query = -1
            return -1

n = int(input())
sorted_list = SortedList()

for _ in range(n):
    operation, x = input().split()
    x = int(x)
    if operation == "+":
        sorted_list.add(x)
    elif operation == "?":
        print(sorted_list.next(x))
