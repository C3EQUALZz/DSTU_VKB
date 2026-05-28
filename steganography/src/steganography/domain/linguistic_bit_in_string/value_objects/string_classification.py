"""StringClassification — результат отнесения одной строки к Y или N."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StringClassification:
    """Строка и её классификация по выбранному стег-методу.

    ``bit`` — скрытый бит сообщения (0 или 1); ``answer`` — словесный
    ответ программы («ДА» для Y-множества, «НЕТ» для N-множества);
    ``feature_value`` — значение лингвистического признака, по которому
    строка отнесена к множеству (для метода по чётности гласных это
    количество гласных букв).
    """

    text: str
    bit: int
    answer: str
    feature_value: int
