# Extended Greatest Common Divisor
def extended_gcd(a, b):
    a, b = abs(a), abs(b)
    A, B, C, D = 1, 0, 0, 1

    while b != 0:
        q, r = divmod(a, b)
        x = A - (q * C)
        y = B - (q * D)
        a, b, A, C, B, D = b, r, C, x, D, y

    return a, A, B


if __name__ == "__main__":
    print(extended_gcd(1234, 54))  # 2, -7, 160
    print(extended_gcd(654137 ** 112, 550))  # 11, -19, 78214...725
    print(extended_gcd(15, 3))  # 3, 0, 1
