"""Эталонные частоты букв русского литературного языка."""

from collections.abc import Mapping
from typing import Final


class RussianLanguageStatistics:
    """Используется кодеком для оценки «русскоязычности» декодированной строки.

    Чем ближе распределение букв в кандидате к эталону, тем выше
    уверенность, что декодирование верное. Для случайного шума,
    равномерно распределённого по алфавиту, значение метрики стремится
    к ≈0.5; для настоящего текста — к ≈1.0.
    """

    _AVERAGE_FREQUENCY: Final[float] = 0.055
    _FREQ: Final[Mapping[str, float]] = {
        "о": 0.1097, "е": 0.0845, "а": 0.0801, "и": 0.0735, "н": 0.0670,
        "т": 0.0626, "с": 0.0547, "р": 0.0473, "в": 0.0454, "л": 0.0440,
        "к": 0.0349, "м": 0.0321, "д": 0.0298, "п": 0.0281, "у": 0.0262,
        "я": 0.0201, "ы": 0.0190, "ь": 0.0174, "г": 0.0170, "з": 0.0165,
        "б": 0.0159, "ч": 0.0144, "й": 0.0121, "х": 0.0097, "ж": 0.0094,
        "ш": 0.0073, "ю": 0.0064, "ц": 0.0048, "щ": 0.0036, "э": 0.0032,
        "ф": 0.0026, "ъ": 0.0004, "ё": 0.0004,
    }

    def letter_frequency(self, ch: str) -> float | None:
        return self._FREQ.get(ch.lower())

    def likeness(self, text: str) -> float:
        counted: int = 0
        weight: float = 0.0
        for ch in text.lower():
            freq: float | None = self._FREQ.get(ch)
            if freq is None:
                continue
            weight += freq
            counted += 1
        if counted == 0:
            return 1.0
        return (weight / counted) / self._AVERAGE_FREQUENCY
