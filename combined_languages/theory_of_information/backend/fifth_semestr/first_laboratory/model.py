import math
import re

from collections import Counter
from typing import Mapping, AnyStr, Final

IGNORE_PATTERN: Final[AnyStr] = r'[^а-яА-Яa-zA-Z0-9 ,.]'

class Model:
    def __init__(self, text: str, ignore_pattern: AnyStr = None) -> None:
        """
        :param text: Строка с текстом для анализа.
        :param ignore_pattern: Паттерн, который надо использовать для игнорирования символов.
        """
        self.text = text

        if ignore_pattern is None:
            self.ignore_pattern = IGNORE_PATTERN
        else:
            self.ignore_pattern = ignore_pattern

    @property
    def text(self) -> AnyStr:
        return self.__text

    @text.setter
    def text(self, user_text: AnyStr) -> None:
        if not isinstance(user_text, str):
            raise ValueError("Ожидается строка в качестве входных данных")
        self.__text = user_text

    @property
    def ignore_pattern(self) -> re.Pattern[AnyStr]:
        return self.__ignore_pattern

    @ignore_pattern.setter
    def ignore_pattern(self, ignore_pattern: str) -> None:
        self.__ignore_pattern = re.compile(ignore_pattern)

    def create_histogram(self) -> dict[str, list[AnyStr] | AnyStr]:
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

    def calculate_character_probabilities(self) -> Mapping[AnyStr, float]:
        """
        Подсчет вероятности символов текста.
        """
        char_counts = Counter()
        total_chars = 0

        # Тут двойная фильтрация, чтобы пользователь мог свою вводить по приколу
        filtered_text = self.ignore_pattern.sub('', string=self.text)

        translation_table = dict.fromkeys(map(ord, '@#$^&*{}[]<><=>=/|=+-"\'«»—…`()№'), None)

        filtered_text = filtered_text.translate(translation_table)

        char_counts.update(filtered_text)
        total_chars += len(filtered_text)

        if total_chars == 0:
            return {}

        return {char: count / total_chars for char, count in char_counts.items()}

    def calculate_entropy(self) -> float:
        """
        Получаем энтропию на основе вероятностей символов.
        """
        probabilities = self.calculate_character_probabilities().values()
        return -1 * sum(probability * math.log2(probability) for probability in probabilities if probability > 0)
