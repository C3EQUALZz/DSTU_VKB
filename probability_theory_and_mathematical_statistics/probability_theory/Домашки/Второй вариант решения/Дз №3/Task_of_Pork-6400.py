from pprint import pprint
from random import randint

x = []
f = []

for i in range(6400):
    for k in range(3):
        y = randint(1, 4)
        y = int(y)
        f.append(y)
        f1 = int("".join(map(str, f)))
    x.append(f1)
    f = []

x.sort()

g = {}
for i in x:
    if i in g:
        g[i] += 1
    else:
        g[i] = 1
pprint(g)

print("---------------------------------------------------------")
max_key = max(g, key=lambda k: g[k])
max(g.items(), key=lambda x: x[1])  # Почему-то не считает
print("Набор чисел", max_key, " встречается максимально часто", max)
min_key = min(g, key=lambda k: g[k])
print("Набор чисел", min_key, " встречается минимальное кол-во раз")
