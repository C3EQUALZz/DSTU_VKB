"""
Вариант 5. Определить понятие «Радиостанция». Состояние объекта определяется следующими полями:
    • наименование радиостанции (строка до 60 символов);
    • частота вещания (вещественное число).
Наименование радиостанции может иметь несколько слов, разделенных пробелами.
Вычислить количество радиостанций, имеющих в своем названии от 2 до 4 слов.
"""

from abc import abstractmethod
from typing import Protocol, List, override


class RadioStation(Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @name.setter
    @abstractmethod
    def name(self, new_name: str) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def frequency(self) -> float:
        raise NotImplementedError

    @frequency.setter
    @abstractmethod
    def frequency(self, new_frequency: float) -> None:
        raise NotImplementedError


class SimpleRadioStation(RadioStation):
    def __init__(self, name: str, frequency: float) -> None:
        self.name: str = name  # Используем сеттер для валидации
        self.frequency: float = frequency

    @property
    @override
    def name(self) -> str:  # type: ignore
        return self._name

    @name.setter
    @override
    def name(self, new_name: str) -> None:
        if len(new_name) > 60:
            raise ValueError("Длина имени не должна превышать 60 символов")
        self._name = new_name

    @property
    @override
    def frequency(self) -> float:  # type: ignore
        return self._frequency

    @frequency.setter
    @override
    def frequency(self, new_frequency: float) -> None:
        if new_frequency < 0:
            raise ValueError("Частота не может быть отрицательной")
        self._frequency = new_frequency


class RadioStationManager:
    def __init__(self) -> None:
        self._stations: List[RadioStation] = []

    def add_station(self, station: RadioStation) -> None:
        self._stations.append(station)

    def count_stations_with_word_range(self, min_words: int = 2, max_words: int = 4) -> int:
        count: int = 0
        for station in self._stations:
            word_count: int = len(station.name.split())
            if min_words <= word_count <= max_words:
                count += 1
        return count


def main() -> None:
    manager: RadioStationManager = RadioStationManager()

    try:
        n: int = int(input("Введите количество радиостанций: "))

        for i in range(n):
            name: str = input(f"Радиостанция {i + 1}. Наименование: ")

            while True:
                try:
                    freq: float = float(input("Частота (вещественное число): "))
                    break
                except ValueError:
                    print("Введите число в формате 100.5")

            manager.add_station(SimpleRadioStation(name, freq))

        word_count: int = manager.count_stations_with_word_range()
        print(f"\nКоличество радиостанций с 2-4 словами в названии: {word_count}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
