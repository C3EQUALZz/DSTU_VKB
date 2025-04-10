"""
Задача №2817. Стильная одежда-2

Глеб обожает шоппинг. Как-то раз он загорелся идеей подобрать себе кепку, майку, штаны и ботинки так,
чтобы выглядеть в них максимально стильно.
В понимании Глеба стильность одежды тем больше, чем меньше разница в цвете элементов его одежды.

В наличии имеется N1 кепок, N2 маек, N3 штанов и N4 пар ботинок (1≤Ni≤100000).
Про каждый элемент одежды известен его цвет (целое число от 1 до 100000).
Комплект одежды — это одна кепка, майка, штаны и одна пара ботинок.
Каждый комплект характеризуется максимальной разницей между любыми двумя его элементами.
Помогите Глебу выбрать максимально стильный комплект, то есть комплект с минимальной разницей цветов.

Входные данные

Для каждого типа одежды i (i=1,2,3,4) сначала вводится количество Ni элементов одежды этого типа,
далее в следующей строке — последовательность из Ni целых чисел, описывающих цвета элементов.
Все четыре типа подаются на вход последовательно, начиная с кепок и заканчивая ботинками.
Все вводимые числа целые, положительные и не превосходят 100000.

Выходные данные

Выведите четыре целых числа — цвета соответственно для кепки, майки, штанов и ботинок,
которые должен выбрать Глеб из имеющихся для того, чтобы выглядеть наиболее стильно.
Если ответов несколько, выведите любой.
"""

from array import ArrayType, array
from copy import copy
from typing import List, Sequence, Tuple


def find_most_stylish_outfit(
    hats: Sequence[int],
    shirts: Sequence[int],
    pants: Sequence[int],
    shoes: Sequence[int],
) -> Tuple[int, int, int, int]:
    """
    Находит наиболее стильный комплект одежды.

    Здесь идет просто перебор с сохранением самого выгодного варианта.
    Самый стартовый вариант - [0, 0, 0, 0].
    В течении работы кода будет меняться не весь список, а отдельные индексы в нем.

    - indices - это массив, который будет использоваться
    - best_indeces - самая удачная конфигурация массива.

    Почему такое условие while? Все очень просто: у нас количество шляп, количество кепок, маек и т.д отличается.
    Сделано с той целью, чтобы не получить IndexError.

    Дальше в теле цикла высчитываем отклонение между максимальным и минимальным.
    Если отклонение минимально, то обновляем массив best_indeces.

    :param hats: Номера шляп.
    :param shirts: Номера маек.
    :param pants: Номера штанов.
    :param shoes: Номера ботинок.
    :returns: Кортеж из индексов массива.
    """
    indices: ArrayType[int] = array("i", [0, 0, 0, 0])
    min_diff: float = float("inf")
    best_indices: ArrayType[int] = array("i", [0, 0, 0, 0])

    while all(
        indices[i] < len(lst) for i, lst in enumerate((hats, shirts, pants, shoes))
    ):
        current_colors = (
            hats[indices[0]],
            shirts[indices[1]],
            pants[indices[2]],
            shoes[indices[3]],
        )
        min_color = min(current_colors)
        max_color = max(current_colors)
        current_diff = max_color - min_color

        # Обновляем минимальную разницу и сохраняем текущие индексы
        if current_diff < min_diff:
            min_diff = current_diff
            best_indices = copy(indices)

        # Если разница минимальна (0), выходим из цикла
        if current_diff == 0:
            break

        # Сдвигаем указатель у минимального элемента
        for i, color in enumerate(current_colors):
            if color == min_color:
                indices[i] += 1
                break

    return (
        hats[best_indices[0]],
        shirts[best_indices[1]],
        pants[best_indices[2]],
        shoes[best_indices[3]],
    )


def main() -> None:
    colors_for_clothes: List[List[int]] = []

    for _ in range(4):
        _ = int(input())
        colors = sorted(map(int, input().split()))
        colors_for_clothes.append(colors)

    stylish_outfit: Tuple[int, int, int, int] = find_most_stylish_outfit(
        *colors_for_clothes
    )
    print(*stylish_outfit)


if __name__ == "__main__":
    main()
