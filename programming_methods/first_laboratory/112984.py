"""
Задача №112984. Гоблины и шаманы

Гоблины Мглистых гор очень любят ходить к своим шаманам. Так как гоблинов много, к шаманам часто образуются очень длинные очереди.
А поскольку много гоблинов в одном месте быстро образуют шумную толку, которая мешает шаманам проводить сложные медицинские манипуляции,
последние решили установить некоторые правила касательно порядка в очереди.

Обычные гоблины при посещении шаманов должны вставать в конец очереди.
Привилегированные же гоблины, знающие особый пароль, встают ровно в ее середину, причем при нечетной длине очереди они встают сразу за центром.

Так как гоблины также широко известны своим непочтительным отношением ко всяческим правилам и законам,
шаманы попросили вас написать программу, которая бы отслеживала порядок гоблинов в очереди.

---

Нельзя все делать с одной очередью, потому что у нас есть момент, когда нужно вставлять в центр (O(n)).
Если будете хранить две очереди примерно равного размера, вставка в середину будет занимать константу.
Остальные операции тоже можно доработать так, чтобы они остались константными.

"""

import collections


q1 = collections.deque()
q2 = collections.deque()

for _ in range(int(input())):

    action = input().split()

    if action[0] == '+':
        q2.append(action[1])
    elif action[0] == '*':
        q2.appendleft(action[1])
    else:
        print(q1.popleft())

    if len(q1) < len(q2):
        q1.append(q2.popleft())

