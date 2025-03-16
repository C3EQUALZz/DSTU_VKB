# Реверс первых N элементов очереди

from collections import deque

# Создайте очередь с некоторыми элементами
q = deque([1, 2, 3, 4, 5])

q.rotate(-3)

print(q)