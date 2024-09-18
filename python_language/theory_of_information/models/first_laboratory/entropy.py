import re
from pathlib import Path
from collections import Counter
from typing import Mapping, SupportsFloat, AnyStr, Final


IGNORE_PATTERN: Final[AnyStr] = r'[@#$^&*{}[\]<>+=/\\|£№]'


def get_character_probabilities(file_path: Path, ignore_pattern: re.Pattern[AnyStr] = None) -> Mapping[AnyStr, SupportsFloat]:
    """

    """
    if not file_path.exists():
        raise FileNotFoundError(f"Нет указанного файла, проверьте корректность {file_path}")

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
