"""
Вариант 2. Определить понятие «Радиостанция». Состояние объекта определяется следующими полями:
    • наименование радиостанции (строка до 60 символов);
    • частота вещания (длинное целое число).
Наименование радиостанции может иметь несколько слов, разделенных пробелами.
В таблице радиостанций изменить название радиостанции, вещающей на заданной частоте.
"""

from abc import abstractmethod
from collections import defaultdict
from typing import Protocol, List, Mapping, Iterable, override


class RadioStation(Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def frequency(self) -> int:
        raise NotImplementedError()

    @frequency.setter
    @abstractmethod
    def frequency(self, frequency: int) -> None:
        raise NotImplementedError()


class SimpleRadioStation(RadioStation):
    def __init__(self, name: str, frequency: int) -> None:
        self.name: str = name
        self.frequency: int = frequency

    @property
    @override
    def frequency(self) -> int:  # type: ignore
        return self.__frequency

    @frequency.setter
    @override
    def frequency(self, frequency: int) -> None:
        self.__frequency: int = frequency

    @property
    @override
    def name(self) -> str:  # type: ignore
        return self.__name

    @name.setter
    @override
    def name(self, new_name: str) -> None:
        if len(new_name) >= 60:
            raise ValueError("Длина имени не должна превышать 60 символов")
        self.__name: str = new_name


class RadioStationManager:
    def __init__(self) -> None:
        self._stations: Mapping[int, List[RadioStation]] = defaultdict(list)

    def add_station(self, station: RadioStation) -> None:
        self._stations[station.frequency].append(station)

    def update_name_by_frequency(self, freq: int, new_name: str) -> int:
        if freq not in self._stations:
            return 0
        for station in self._stations[freq]:
            station.name = new_name
        return len(self._stations[freq])

    @property
    def stations(self) -> Iterable[RadioStation]:
        all_stations: List[RadioStation] = []
        for stations in self._stations.values():
            all_stations.extend(stations)
        return all_stations


def main() -> None:
    manager: RadioStationManager = RadioStationManager()

    try:
        n: int = int(input("Введите количество радиостанций: "))

        for i in range(n):
            name: str = input(f"Радиостанция {i + 1}. Наименование: ")

            while True:
                try:
                    freq: int = int(input("Частота (целое число): "))
                    break
                except ValueError:
                    print("Введите целое число")

            manager.add_station(SimpleRadioStation(name, freq))

        print("\nВведите частоту для изменения названия:")
        target_freq: int = int(input("Целевая частота: "))
        new_name: str = input("Новое название: ")

        updated_count: int = manager.update_name_by_frequency(target_freq, new_name)
        print(f"\nОбновлено {updated_count} радиостанций")

        print("\nТекущий список радиостанций:")
        for station in manager.stations:
            print(f"{station.name} ({station.frequency} кГц)")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
