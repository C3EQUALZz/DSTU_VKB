from typing import Any

"""
Модуль показывает алгоритмы, которые превращают из вложенных структур данных в одномерный. 
"""


def flatten(lst: list[[list, ...]]) -> list[Any]:
    """
    Перевод из многомерного в итератор одномерный
    :param lst: многомерный список
    :return: итератор
    """
    for i in lst:
        yield from flatten(i) if isinstance(i, list) else (i,)


# Перевод в одномерный список
linear = lambda data: [data] if isinstance(data, int) else sum(map(linear, data), [])


def flatten_dict(d: dict, parent_key: str = '', sep: str = '_'):
    """
    Этот код рекурсивно проходит по всем элементам многомерного словаря и преобразует его в одномерный словарь,
    где ключи состоят из исходных ключей, разделенных разделителем (по умолчанию "_"), а значениями являются
    соответствующие значения. :param d: :param parent_key: :param sep: :return:
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)