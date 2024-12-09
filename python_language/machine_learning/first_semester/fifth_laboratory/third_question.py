"""
1. Сгенерируйте Series из 100 значений нормально распределённой СВ (np.random.normal с дефолтными параметрами - нулевым средним и единичной дисперсией).
2. Возведите каждое значение серии в 3 степень, а значения индекса увеличьте в 3 раза.
3. Выведите сумму элементов, строго меньших 2.6, имеющих нечётные значения индекса.
4. Выведите количество значений серии меньше нуля.

- Следует внимательнее использовать [ ] для выбора данных по нескольким условиям:
 либо выбирать данные последовательно, либо сразу по нескольким условиям, но через оператор &.
Отличие оператора and от оператора &: and - выводит последнее проверенное значение, & - выводит пересечение значений.
Пример: s[ _  &  _ ].sum()
"""
import numpy as np
import pandas as pd
from typing import Any, Callable

np.random.seed(242)


def raise_to_the_power_and_increase_index(old_series: pd.Series) -> pd.Series:
    new_series = pd.Series(old_series) ** 3
    new_series.index *= 3
    return new_series


def func_with_predicate(series: pd.Series, predicate: Any, func: Callable[[pd.Series], int]) -> int:
    return func(series[predicate])


def main() -> None:
    series = pd.Series(data=np.random.normal(size=100))

    print(
        "Series: ", series,
        "Новый Series, где каждое значение возведено в 3 степень и значения индексов в 3 раза больше: ",
        new := raise_to_the_power_and_increase_index(series),
        "Сумма элементов, строго меньших 2.6, имеющих нечётные значения индекса: ",
        func_with_predicate(new, lambda s: (s < 2.6) & (s.index % 2 != 0), pd.Series.sum),
        "Количество значений серии меньше нуля.",
        func_with_predicate(new, lambda s: s < 0, len),
        sep="\n\n"
    )


if __name__ == '__main__':
    main()
