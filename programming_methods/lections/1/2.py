# Первые неповторяющиеся целые числа в массиве
from functools import reduce
from operator import xor

a = [1, 2, 1, 2, 3]

print(reduce(xor, a))
