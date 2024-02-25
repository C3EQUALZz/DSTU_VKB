"""
Здесь описана логика создания графиков Хи-квадрат распределения и распределения Стьюдента
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, t
from typing import Final, Any

# Константы, которые описывают конечные значения осей
X_RANGE_CHI_SQUARE: Final = (0, 20)
X_RANGE_T_DISTRIBUTION: Final = (-15, 15)
Y_LIMITS_CHI_SQUARE: Final = (0, 1)
Y_LIMITS_T_DISTRIBUTION: Final = (0, 0.48)


def chi_square_distribution(graphic) -> None:
    """
    Построение графиков хи-квадрат распределения
    """
    # Определение диапазона значений для оси x
    x = np.linspace(*X_RANGE_CHI_SQUARE, 150)

    for df in [1, 2, 3, 5, 10]:
        graphic.plot(x, chi2.pdf(x, df), label=f'Хи-квадрат распределение с k = {df}')

    graphic.set_xlim(X_RANGE_CHI_SQUARE)
    graphic.set_ylim(Y_LIMITS_CHI_SQUARE)


def t_distribution(graphic) -> None:
    """
    Построение графика t-распределения
    """
    # Определение диапазона значений для оси x
    x = np.linspace(*X_RANGE_T_DISTRIBUTION, 1000)

    for df in [1, 3, 5, 9, 20, 25]:
        graphic.plot(x, t.pdf(x, df=df), label=f'Распределение Стьюдента с k = {df}')

    graphic.set_xlim(X_RANGE_T_DISTRIBUTION)
    graphic.set_ylim(Y_LIMITS_T_DISTRIBUTION)

    # Перемещаем оси в центр, чтобы адекватно выглядело
    for spine in ("left", "bottom"):
        graphic.spines[spine].set_position("zero")


def main() -> None:
    """
    Точка запуска программы, отсюда происходит запуск двух функций, объединение на 1 фото, установка общих параметров
    """

    # Создание сетки подграфиков 2x1
    fig, axs = plt.subplots(2, 1, figsize=(11.69, 8.27))

    # Само место для (место для графика, функция обработки распределения, название)
    zipped_arguments: tuple[Any, callable, str] = zip(
        axs,
        (chi_square_distribution, t_distribution),
        ("Хи-квадрат распределение", "Распределение Стьюдента")
    )

    # Устанавливаем подписи для осей, включаем сетку, устанавливаем имена для графиков
    for graphic, function, name in zipped_arguments:
        graphic.set_xlabel('x')
        graphic.set_ylabel('p(x)')
        graphic.grid(True)
        graphic.set_title(name)
        function(graphic)
        graphic.legend(loc='upper right', fontsize='x-small', frameon=True)

    # Отображение графика с отступами
    plt.subplots_adjust(top=0.87, bottom=0.1, left=0.13, right=0.9, hspace=0.5, wspace=0.3)
    # Сохранение графика в формате PDF
    plt.savefig('distributions_a4.pdf', format='pdf')


if __name__ == '__main__':
    main()
