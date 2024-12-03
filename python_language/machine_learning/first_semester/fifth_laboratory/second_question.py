"""
По клиенту получены зашумленные данные (объект s типа Series) по его транзакциям.

Для заданного ниже объекта s проделайте следующее:
1. Создайте новый Series, значения которого совпадают со значениями s, а индексы - целочисленные значения от 2 до 12, не включая 12.
2. Выберите из s элементы с индексами 3 и 5, после чего просуммируйте их, сохранив результат.
3. Выберите из s только целочисленные элементы и вычислите их дисперсию.

Все полученные результаты округлите до 2-х знаков после запятой.

Пояснения:
3. Целочисленные значения - значения, имеющие тип int.
- Дисперсия рассчитывается с помощью функции из библиотеки numpy:
np.var(, ddof=0) или встроенной в python функции: .var(ddof=1)
"""
import pandas as pd
import numpy as np


def create_new_series(s: pd.Series, start: int = 2, end: int = 12) -> pd.Series:
    new_index = range(start, end)
    return pd.Series(s.values, index=new_index)


def sum_selected_elements(s: pd.Series, indices: tuple[int, int]) -> float:
    try:
        return round(s[indices[0]] + s[indices[1]], 2)
    except TypeError as err:
        print(f"All values must be int or float for correct work, error: {err}")
        return s[indices[0]]


def variance_of_integer_elements(s: pd.Series) -> float:
    integer_elements = s[s.apply(lambda x: isinstance(x, int))]
    return round(np.var(integer_elements, ddof=0), 2)


def main() -> None:
    s = pd.Series(data=['1', 2, 3.1, 'hi!', 5, -512, 12.42, 'sber', 10.10, 98],
                  index=range(6, 26, 2))

    new_series = create_new_series(s)
    print(
        "Old Series:", s,
        "New Series:", new_series,
        "Sum of elements at indices 3 and 5:", sum_selected_elements(new_series, (3, 5)),
        "Variance of integer elements:", variance_of_integer_elements(new_series),
        sep="\n\n"
    )

if __name__ == '__main__':
    main()
