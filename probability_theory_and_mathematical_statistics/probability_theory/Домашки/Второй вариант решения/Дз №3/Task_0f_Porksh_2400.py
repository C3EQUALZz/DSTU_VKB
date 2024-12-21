from random import randint
import random
from pprint import pprint

x = []
f = []

for i in range(2400):
    y = randint(1, 3)
    y = int(y)
    if y == 3:
        f.append(y)
        f1 = int(''.join(map(str, f)))
        y = randint(1, 2)
        y = int(y)
        if y == 1:
            f.append(y)
            f1 = int(''.join(map(str, f)))
            f.append(2)
            f1 = int(''.join(map(str, f)))
        if y == 2:
            f.append(y)
            f1 = int(''.join(map(str, f)))
            f.append(1)
            f1 = int(''.join(map(str, f)))
        y = int(y)
    elif y == 2:
        f.append(y)
        f1 = int(''.join(map(str, f)))
        u = [1, 3]
        y = random.choice(u)
        y = int(y)
        if y == 1:
            f.append(y)
            f1 = int(''.join(map(str, f)))
            f.append(3)
            f1 = int(''.join(map(str, f)))
        if y == 3:
            f.append(y)
            f1 = int(''.join(map(str, f)))
            f.append(1)
            f1 = int(''.join(map(str, f)))
        y = int(y)
    elif y == 1:
        y = int(y)
        f.append(y)
        y = randint(2, 3)
        if y == 2:
            y = int(y)
            f.append(y)
            f1 = int(''.join(map(str, f)))
            f.append(3)
            f1 = int(''.join(map(str, f)))
        if y == 3:
            y = int(y)
            f.append(y)
            f1 = int(''.join(map(str, f)))
            f.append(2)
            f1 = int(''.join(map(str, f)))

        y = int(y)
    x.append(f1)
    f = []

#print(x)
x.sort()

g = {}
for i in x:
    if i in g:
        g[i] += 1
    else:
        g[i] = 1
pprint(g)