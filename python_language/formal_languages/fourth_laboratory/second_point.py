def leftFactoring(s):
    k = []
    l = []
    n = ""
    k = s.split('->')
    l = k[1].split('/')
    for i in range(0, len(l) - 1):
        for j in range(0, min(len(l[i]), len(l[i + 1]))):
            if(l[i][j] == l[i + 1][j]):
                if l[i][j] not in n:
                    n = n + l[i][j]
    print(k[0] + '->' + n + "R")
    m = k[1].split(n)
    print("R->", end="")
    for i in range(1, len(m)):
        print(m[i], end="")

s = input("Enter the production: ")
while True:
    leftFactoring(s)
    print("\ndo you have another production?")
    T = input("y/n:")
    if T == 'y':
        s = input("Enter the production: ")
    elif T == 'n':
        break