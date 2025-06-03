from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, List, override


class RadioStation(Protocol):
    @abstractmethod
    def is_in_frequency_range(
            self,
            min_freq: float,
            max_freq: float
    ) -> bool:
        """Проверяет, находится ли частота станции в заданном диапазоне"""
        raise NotImplementedError


@dataclass
class SimpleRadioStation(RadioStation):
    name: str
    frequency: float

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or len(self.name) >= 60:
            raise ValueError("Неправильные данные для радиостанции")

    @override
    def is_in_frequency_range(self, min_freq: float, max_freq: float) -> bool:
        return min_freq <= self.frequency <= max_freq


class RadioStationManager:
    def __init__(self) -> None:
        self._stations: List[RadioStation] = []

    def add_station(self, station: RadioStation) -> None:
        self._stations.append(station)

    def count_in_frequency_range(self, min_freq: float, max_freq: float) -> int:
        return sum(1 for station in self._stations if station.is_in_frequency_range(min_freq, max_freq))


def main() -> None:
    manager: RadioStationManager = RadioStationManager()

    while True:
        try:
            n: int = int(input("Введите количество радиостанций: "))

            for i in range(n):
                name: str = input(f"Радиостанция {i + 1}. Наименование: ")

                while True:
                    try:
                        freq: float = float(input("Частота: "))
                        break
                    except ValueError:
                        print("Введите число в формате 100.5")

                manager.add_station(SimpleRadioStation(name, freq))

            print("\nВведите диапазон частот для поиска:")
            min_freq: float = float(input("Минимальная частота: "))
            max_freq: float = float(input("Максимальная частота: "))

            result: int = manager.count_in_frequency_range(min_freq, max_freq)
            print(f"\nКоличество радиостанций в диапазоне: {result}")

        except ValueError as e:
            print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
