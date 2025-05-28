"""
Вычислить НОД(a, b) при помощи алгоритма Евклида с делением с остатком;
"""


class GCDMod(GCDStrategy):
    def __init__(self) -> None:
        self.__iterations = 0

    def compute(self, a: NumberType, b: NumberType) -> NumberType:
        ...

    def iterations(self) -> NumberType:
        ...

def gcd(
        a: NumberType,
        b: NumberType
) -> NumberType:
    """

    Args:
        a:
        b:

    Returns:

    """
    a: NumberType = abs(a)
    b: NumberType = abs(b)

    while b != 0:
        a, b = b, a % b

    return a
