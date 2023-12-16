"""
В данном модуле реализация 7 задания, где нужно написать классы, связанные с животными
"""
__all__ = ["Carnivore", "Omnivore", "Herbivore", "Animal"]

from abc import ABC, abstractmethod
from functools import total_ordering
from random import randint
from typing import TypeVar, Self
import json

Animal = TypeVar('Animal')


@total_ordering
class Animal(ABC):
    """
    Родительский класс, который описывает животное
    """

    def __init__(self, identifier: int, name: str) -> None:
        self.identifier = identifier
        self.name = name

    def __lt__(self, other: Animal) -> bool:
        """
        Магический метод для оператора <
        """
        return (self.calculate_weight(self.food_requirements()), self.name) < (
            self.calculate_weight(other.food_requirements()), other.name)

    def __eq__(self, other: Animal) -> bool:
        """
        Магический метод для оператора ==
        """
        return (self.calculate_weight(self.food_requirements()), self.name) == (
            self.calculate_weight(other.food_requirements()), other.name)

    @abstractmethod
    def food_requirements(self) -> str:
        """
        Аб
        """
        ...

    @abstractmethod
    def serialize_data(self):
        ...

    def deserialize_data(self, data: dict) -> Self:
        ...

    @classmethod
    def animal_to_dict(cls, obj):
        if isinstance(obj, cls):
            return {
                'identifier': obj.identifier,
                'name': obj.name,
                'type': obj.__class__.__name__,
                'data': obj.serialize_data(),
            }
        return None

    @classmethod
    def dict_to_animal(cls, data):
        if 'type' in data and data['type'] == cls.__name__:
            return cls(data['identifier'], data['name']).deserialize_data(data['data'])
        return None

    def to_json(self):
        return json.dumps(self, default=self.animal_to_dict, indent=2)

    @classmethod
    def from_json(cls, json_data):
        return json.loads(json_data, object_hook=cls.dict_to_animal)

    @staticmethod
    def calculate_weight(food_requirements: str) -> int:
        return sum(map(int, filter(lambda substring: substring.isdigit(), food_requirements.split())))


class Carnivore(Animal):
    """
    Класс, который описывает хищников
    """

    def __init__(self, identifier: int, name: str) -> None:
        super().__init__(identifier, name)
        self.random_weight_meat = randint(20, 50)

    def serialize_data(self):
        return {'random_weight_meat': self.random_weight_meat}

    def deserialize_data(self, data):
        self.random_weight_meat = data['random_weight_meat']
        return self

    def food_requirements(self) -> str:
        return f"{self.name} требуется {self.random_weight_meat}кг мяса."


class Omnivore(Animal):
    """
    Класс, который описывает всеядных животных
    """

    def __init__(self, identifier: int, name: str) -> None:
        super().__init__(identifier, name)
        self.random_weight_meat, self.random_weight_grass = randint(20, 50), randint(20, 50)

    def serialize_data(self):
        return {'random_weight_meat': self.random_weight_meat, 'random_weight_grass': self.random_weight_grass}

    def deserialize_data(self, data):
        self.random_weight_meat = data['random_weight_meat']
        self.random_weight_grass = data['random_weight_grass']
        return self

    def food_requirements(self) -> str:
        return f"{self.name} требуется микс {self.random_weight_meat}кг мяса и {self.random_weight_grass}кг травы."


class Herbivore(Animal):
    """
    Класс, который описывает травоядных животных
    """

    def __init__(self, identifier: int, name: str) -> None:
        super().__init__(identifier, name)
        self.random_weight_grass = randint(20, 50)

    def serialize_data(self):
        return {'random_weight_grass': self.random_weight_grass}

    def deserialize_data(self, data):
        self.random_weight_grass = data['random_weight_grass']
        return self

    def food_requirements(self) -> str:
        return f"{self.name} потребляет {self.random_weight_grass}кг травы."
