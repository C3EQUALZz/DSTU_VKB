"""
Вариант 4. Определить понятие «Радиостанция». Состояние объекта определяется следующими полями:
    • наименование радиостанции (строка до 60 символов);
    • частота вещания (вещественное число).
Наименование радиостанции может иметь несколько слов, разделенных пробелами.
Вычислить количество радиостанций, имеющих в своем названии сочетание букв «музыка».
"""

from abc import abstractmethod
from typing import Protocol, List, override


# Протокол для радиостанции
class RadioStation(Protocol):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @name.setter
    @abstractmethod
    def name(self, new_name: str) -> None:
        ...

    @property
    @abstractmethod
    def frequency(self) -> float:
        ...

    @frequency.setter
    @abstractmethod
    def frequency(self, new_frequency: float) -> None:
        ...


# Конкретная реализация радиостанции
class SimpleRadioStation(RadioStation):
    def __init__(self, name: str, frequency: float) -> None:
        self._name: str = ""
        self._frequency: float = 0.0
        self.name = name  # Используем сеттер для валидации
        self.frequency = frequency

    @property
    @override
    def name(self) -> str: # type: ignore
        return self._name

    @name.setter
    @override
    def name(self, new_name: str) -> None:
        if len(new_name) > 60:
            raise ValueError("Длина имени не должна превышать 60 символов")
        self._name = new_name

    @property
    @override
    def frequency(self) -> float: # type: ignore
        return self._frequency

    @frequency.setter
    @override
    def frequency(self, new_frequency: float) -> None:
        if new_frequency < 0:
            raise ValueError("Частота не может быть отрицательной")
        self._frequency = new_frequency


# Менеджер для работы с радиостанциями
class RadioStationManager:
    def __init__(self) -> None:
        self._stations: List[RadioStation] = []

    def add_station(self, station: RadioStation) -> None:
        self._stations.append(station)

    def count_stations_with_music(self) -> int:
        count = 0
        for station in self._stations:
            if "музыка" in station.name.lower():
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

        music_count: int = manager.count_stations_with_music()
        print(f"\nКоличество радиостанций с 'музыка' в названии: {music_count}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
