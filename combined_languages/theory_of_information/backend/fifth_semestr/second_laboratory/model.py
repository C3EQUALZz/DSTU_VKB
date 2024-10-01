import math

from collections import Counter
from typing import Mapping, AnyStr, TypeVar, Generic, Union

T = TypeVar('T', bound=Union[str, bytes])

class Model(Generic[T]):
    def __init__(self, text: T) -> None:
        """
        :param text: Строка с текстом для анализа.
        """
        self.text = text

    @property
    def text(self) -> T:
        return self.__text

    @text.setter
    def text(self, user_text: T) -> None:
        if not isinstance(user_text, (bytes, str)):
            raise ValueError("Ожидается строка в качестве входных данных")
        self.__text = user_text


    def create_histogram(self) -> dict[str, list[int | float] | AnyStr]:
        """
        Создаем и возвращаем JSON с гистограммой вероятностей символов.
        """
        probabilities = self.calculate_character_probabilities()

        characters = list(probabilities.keys())
        values = list(probabilities.values())

        return {
            "x": characters,
            "y": values,
            "type": "bar"
        }

    def calculate_character_probabilities(self) -> Mapping[int, float]:
        """
        Подсчет вероятности символов текста.
        """
        char_counts = Counter(self.text)
        total_chars = len(self.text)

        if total_chars == 0:
            return {}

        return {char: count / total_chars for char, count in char_counts.items()}

    def calculate_entropy(self) -> float:
        """
        Получаем энтропию на основе вероятностей символов.
        """
        probabilities = self.calculate_character_probabilities().values()
        return -1 * sum(probability * math.log2(probability) for probability in probabilities if probability > 0)
