import math
import re

from collections import Counter
from pathlib import Path
from typing import Mapping, AnyStr, Final

IGNORE_PATTERN: Final[AnyStr] = r'[@#$^&*{}[\]<>+=/\\|£№]'


class Model:

    def create_histogram(self, file_path: Path, ignore_pattern):
        probabilities = self.calculate_character_probabilities(file_path, ignore_pattern)


    @staticmethod
    def calculate_character_probabilities(
            file_path: Path,
            ignore_pattern: re.Pattern[AnyStr] = None
    ) -> Mapping[AnyStr, float]:

        """
        Подсчет вероятности символов текста из файла.
        :param file_path: Путь до txt файла с текстом.
        :param ignore_pattern: Паттерн, который надо использовать для игнорирования текста
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Нет указанного файла, проверьте корректность {file_path}")

        if file_path.suffix.lower() != '.txt':
            raise ValueError(f"Поддерживается работа только с txt файлами")

        if ignore_pattern is None:
            ignore_pattern = IGNORE_PATTERN

        char_counts = Counter()
        total_chars = 0

        with file_path.open('r', encoding='utf-8') as file:
            for row in file:
                filtered_text = re.sub(ignore_pattern, '', row)
                char_counts.update(filtered_text)
                total_chars += len(filtered_text)

        if total_chars == 0:
            return {}

        return {char: count / total_chars for char, count in char_counts.items()}

    @staticmethod
    def calculate_entropy(
            dictionary: Mapping[AnyStr, float]
    ) -> float:
        """
        Получаем энтропию, зная вероятности каждого символа
        :param dictionary: словарь с вероятностями появления каждого символа
        """
        probabilities = dictionary.values()
        return -1 * sum(probability * math.log2(probability) for probability in probabilities)


