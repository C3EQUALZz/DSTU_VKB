from decimal import Decimal


def gcd(a: Decimal, b: Decimal):
    """
    Вычисление НОД
    Наибольший общий делитель
    """
    while a != 0 and b != 0:
        if abs(a) > abs(b):
            a %= b
        else:
            b %= a
    return a + b


def lcm(a: Decimal, b: Decimal):
    """
    Наименьшее общее кратное (НОК)
    Наименьшее натуральное число,
    которое делится на каждое из этих чисел.
    """
    if abs(a) == 1 or abs(b) == 1:
        return a
    return a * b // gcd(a, b)


if __name__ == "__main__":
    try:
        a, b = map(Decimal, input("Введите 2 числа: ").split())
        print(f"НОД двух чисел {gcd(a, b)}", f"НОК двух чисел {lcm(a, b)}", sep='\n')
    except ValueError:
        print("Неверный тип данных")
