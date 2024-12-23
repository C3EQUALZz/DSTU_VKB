"""
1. Создайте Series из последовательности 15 значений, равномерно разбивающих отрезок [0, 20] (воспользуйтесь функцией linspace)
2. Определите отношение элементов полученной серии к их предыдущим элементам.
3. В результате необходимо получить среднее полученного вектора, оставив в нём только те значения, которые не более чем 1.5.

Пояснения:
2. Если было бы необходимо найти последовательность из 3-х значений,
равномерно разбивающих отрезок [0,1], то это были бы значения [0, 0.5, 1].
3. Если был бы дан список элементов a = [1,2,3,12], отношения элементов к предыдущим будут равны [NaN, 2, 1.5, 4].
А на последнем этапе в таком примере останется только [1.5] и среднее значение будет также 1.5.
"""
import numpy as np
import pandas as pd


def calculate_ratios(series: pd.Series, shift: int = 1) -> pd.Series:
    return series / series.shift(shift)


def mean_of_filtered_ratios(series: pd.Series, threshold: float = 1.5) -> float:
    ratios = calculate_ratios(series)
    filtered_ratios = ratios[ratios <= threshold]
    return filtered_ratios.mean()


def main() -> None:
    series = pd.Series(np.linspace(0, 20, 15))

    print("Series:", series,
          "Отношение к прошлым элементам", calculate_ratios(series),
          "Среднее после фильтрации (<= 1.5):", mean_of_filtered_ratios(series),
          sep='\n\n')


if __name__ == '__main__':
    main()
