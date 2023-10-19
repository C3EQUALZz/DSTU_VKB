"""
Данный код проверяет на соответствие тому, что число палиндром.
Палиндром - число или строка одинаковая, если развернуть наоборот.

>>> check_palindromes(15)
False
>>> check_palindromes(222)
True
>>> check_palindromes(1515)
False
"""


def check_palindromes(element: str):

    if not isinstance(element, str):
        element = str(element)

    # идем до половины, так как дальше нет смысла
    for i in range(len(element) // 2):
        if element[i] != element[~i]:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()