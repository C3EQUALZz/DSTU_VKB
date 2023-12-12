"""
Реализация класса Train, Trains
"""

__all__ = ["Train", "Trains"]

from bisect import bisect_left
########################################################################################################################
from dataclasses import dataclass
from functools import total_ordering
from typing import TypeVar

########################################################################################################################
import numpy as np
from arrow import Arrow

########################################################################################################################
Train = TypeVar("Train")


@dataclass
@total_ordering
class Train:
    """
    Данный класс описывает именно один поезд
    """
    dest: str
    number: int
    departure: Arrow.time

    def __lt__(self, other: Train) -> bool:
        """
        Магический метод, который проверяет меньше ли первый поезд второго по месту назначения
        по лексикографическому порядку.
        Все остальные сравнения добавит декоратор total_ordering
        """
        if isinstance(other, self.__class__):
            return self.departure < other.departure
        return NotImplemented

    def __eq__(self, other: Train) -> bool:
        """
        Магический метод, который сравнивает два поезда по отправлению.
        Все оставшиеся сравнения добавит total_ordering
        """
        if isinstance(other, self.__class__):
            return self.departure == other.departure
        return NotImplemented

    @property
    def info(self) -> str:
        """
        Свойство, которое возвращает информацию о поезде
        """
        return f"Поезд №{self.number} отправляется в {self.dest} в {self.departure}"


class Trains:
    """
    Данный класс описывает сущность всех поездов
    Станция???
    """

    def __init__(self, trains: np.ndarray[Train, ...]) -> None:
        self.trains: np.ndarray[Train, ...] = trains

    def __getitem__(self, item: int) -> np.ndarray[Train, ...] | str | Train:
        """
        Магический метод, который позволяет обращаться к элементу по индексу
        """
        return self.trains[item]

    @property
    def trains(self) -> np.ndarray[Train, ...]:
        """
        Свойство, с помощью которого мы можем получать все поезда
        """
        return self._trains

    @trains.setter
    def trains(self, trains: np.ndarray[Train, ...]):
        """
        Свойство, с помощью которого мы устанавливаем поезда в качестве атрибута, сортируя перед этим
        """
        sorting_indexes = np.argsort([train.number for train in trains])
        self._trains = trains[sorting_indexes]

    def sort(self, key: callable = None) -> None:
        """
        Метод, который сортирует массив по заданному ключу
        """
        self._trains = np.array(sorted(self.trains, key=key))

    def find(self, target_number: int) -> int:
        """
        Метод, который ищет поезд по номеру. Используется бинарный поиск для определения номера.
        """
        index = bisect_left([train.number for train in self.trains], target_number)
        if 0 <= index < len(self.trains) and self.trains[index].number == target_number:
            return index
        raise IndexError("Ошибка с выбором индекса для поезда")
