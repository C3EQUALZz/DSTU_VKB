"""FormattingDetector — находит несущий параметр форматирования."""

from collections import Counter

from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)


class FormattingDetector:
    """Перебирает параметры форматирования и выбирает подходящий метод.

    Параметр считается носителем сокрытия, если по всему контейнеру он
    принимает ровно два значения. Среди нескольких таких кандидатов
    выигрывает тот, у которого «единичное» значение встречается чаще —
    при равной частоте берётся первый по порядку перечисления.
    """

    def detect(
        self,
        chars: list[FormattedChar],
    ) -> FormattingMethod | None:
        candidates: list[FormattingMethod] = []
        for param in FormattingParam:
            counter: Counter[str] = Counter(
                c.attrs[param] for c in chars if param in c.attrs
            )
            if len(counter) != 2:
                continue
            (zero_value, _), (one_value, ones_cnt) = counter.most_common(2)
            if ones_cnt < 1:
                continue
            candidates.append(
                FormattingMethod(
                    param=param,
                    zero_value=zero_value,
                    one_value=one_value,
                ),
            )
        if not candidates:
            return None
        candidates.sort(
            key=lambda m: _signal_strength(chars, m), reverse=True,
        )
        return candidates[0]


def _signal_strength(
    chars: list[FormattedChar],
    method: FormattingMethod,
) -> int:
    return sum(
        1
        for c in chars
        if c.attrs.get(method.param) == method.one_value
    )
