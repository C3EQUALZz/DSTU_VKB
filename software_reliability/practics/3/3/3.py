"""
Определить понятие «Радиостанция». Состояние объекта определяется следующими полями:
    • наименование радиостанции (строка до 60 символов);
    • частота вещания (длинное целое число).
Наименование радиостанции может иметь несколько слов, разделенных пробелами.
В таблице радиостанций изменить частоту вещания радиостанции с заданным названием.
"""

from abc import abstractmethod
from typing import Protocol, List, Iterable, override


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
    def frequency(self) -> int:
        ...

    @frequency.setter
    @abstractmethod
    def frequency(self, new_frequency: int) -> None:
        ...


class SimpleRadioStation(RadioStation):
    def __init__(self, name: str, frequency: int) -> None:
        self.name: str = name  # Используем сеттер для валидации
        self.frequency: int = frequency

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
    def frequency(self) -> int:  # type: ignore
        return self._frequency

    @frequency.setter
    @override
    def frequency(self, new_frequency: int) -> None:
        if new_frequency < 0:
            raise ValueError("Частота не может быть отрицательной")
        self._frequency = new_frequency


# Менеджер для работы с радиостанциями
class RadioStationManager:
    def __init__(self) -> None:
        self._stations: List[RadioStation] = []

    def add_station(self, station: RadioStation) -> None:
        self._stations.append(station)

    def update_frequency_by_name(self, target_name: str, new_frequency: int) -> int:
        count: int = 0
        for station in self._stations:
            if station.name == target_name:
                station.frequency = new_frequency
                count += 1
        return count

    @property
    def stations(self) -> Iterable[RadioStation]:
        return self._stations


def main() -> None:
    manager: RadioStationManager = RadioStationManager()

    try:
        n: int = int(input("Введите количество радиостанций: "))

        for i in range(n):
            name: str = input(f"Радиостанция {i + 1}. Наименование: ")

            while True:
                try:
                    freq: int = int(input("Частота (длинное целое число): "))
                    break
                except ValueError:
                    print("Введите целое число")

            manager.add_station(SimpleRadioStation(name, freq))

        print("\nВведите наименование радиостанции для изменения частоты:")
        target_name: str = input("Название радиостанции: ")
        while True:
            try:
                new_freq: int = int(input("Новая частота: "))
                break
            except ValueError:
                print("Введите целое число")

        updated_count: int = manager.update_frequency_by_name(target_name, new_freq)
        print(f"\nОбновлено {updated_count} радиостанций")

        print("\nТекущий список радиостанций:")
        for station in manager.stations:
            print(f"{station.name} ({station.frequency} кГц)")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
