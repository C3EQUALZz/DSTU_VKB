"""
Вариант 6 Определить понятие «Радиостанция». Состояние объекта определяется следующими полями:
• наименование радиостанции (строка до 60 символов);
• частота вещания (длинное целое число).
Наименование радиостанции может иметь несколько слов, разделенных пробелами.
Составляется заявка на распределение частот вещания. Проверить таблицу радиостанций на корректность.
Сформировать и вывести на экран наименования радиостанций, подавших заявки на вещание на совпадающих
частотах. При отсутствии конфликтов выдать сообщение «Норма».
"""

from abc import abstractmethod
from collections import defaultdict
from typing import Protocol, List, Dict, override


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
    def frequency(self) -> int:
        ...

    @frequency.setter
    @abstractmethod
    def frequency(self, new_frequency: int) -> None:
        ...


# Конкретная реализация радиостанции
class SimpleRadioStation(RadioStation):
    def __init__(self, name: str, frequency: int) -> None:
        self.name: str = name
        self.frequency: int = frequency

    @property
    @override
    def name(self) -> str: # type: ignore
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if len(new_name) > 60:
            raise ValueError("Длина имени не должна превышать 60 символов")
        self._name: str = new_name

    @property
    @override
    def frequency(self) -> int: # type: ignore
        return self._frequency

    @frequency.setter
    def frequency(self, new_frequency: int) -> None:
        if new_frequency < 0:
            raise ValueError("Частота не может быть отрицательной")
        self._frequency: int = new_frequency


# Менеджер для работы с радиостанциями
class RadioStationManager:
    def __init__(self) -> None:
        self._stations_by_frequency: Dict[int, List[RadioStation]] = defaultdict(list)

    def add_station(self, station: RadioStation) -> None:
        self._stations_by_frequency[station.frequency].append(station)

    def get_conflicting_stations(self) -> Dict[int, List[RadioStation]]:
        # Возвращаем только те частоты, где более одной станции
        return {freq: stations for freq, stations in self._stations_by_frequency.items() if len(stations) > 1}


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

        conflicts: Dict[int, List[RadioStation]] = manager.get_conflicting_stations()

        if not conflicts:
            print("\nНорма")
        else:
            print("\nКонфликтующие частоты:")
            for freq, stations in conflicts.items():
                station_names: List[str] = [station.name for station in stations]
                print(f"{freq} кГц: {', '.join(station_names)}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
