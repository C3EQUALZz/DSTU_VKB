"""FormattingDetector — находит несущий параметр форматирования."""

from collections import Counter

from steganography.domain.common.services.formatting_shift import (
    shifted_value,
)
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)

# Параметры с относительной дельтой — для парного режима детекции.
_SHIFTABLE: tuple[FormattingParam, ...] = (
    FormattingParam.SIZE,
    FormattingParam.COLOR,
    FormattingParam.SCALE,
    FormattingParam.SPACING,
)


class FormattingDetector:
    """Перебирает параметры форматирования и выбирает подходящий метод.

    Параметр считается носителем сокрытия, если по всему контейнеру он
    принимает ровно два значения. Среди нескольких таких кандидатов
    выигрывает тот, у которого «единичное» значение встречается чаще —
    при равной частоте берётся первый по порядку перечисления.

    Если простых кандидатов нет, включается парный режим: значения
    раскладываются на пары «база / база+дельта» — так выглядит сокрытие
    относительной дельтой в контейнере с несколькими стилями текста.
    """

    def detect(
        self,
        chars: list[FormattedChar],
    ) -> FormattingMethod | None:
        counters = {
            param: Counter(c.attrs[param] for c in chars if param in c.attrs)
            for param in FormattingParam
        }
        candidates: list[FormattingMethod] = []
        for param in FormattingParam:
            counter = counters[param]
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
            # Парный режим: сокрытие относительной дельтой от исходного
            # форматирования — значений больше двух, но они раскладываются
            # на пары «база / база+дельта» (неоднородный контейнер).
            for param in _SHIFTABLE:
                method = _detect_pairs(param, counters[param])
                if method is not None:
                    candidates.append(method)
        if not candidates:
            return None
        candidates.sort(
            key=lambda m: _signal_strength(chars, m), reverse=True,
        )
        return candidates[0]


def _detect_pairs(
    param: FormattingParam,
    counter: Counter[str],
) -> FormattingMethod | None:
    """Раскладывает значения параметра на пары «база / база+дельта».

    Срабатывает, только если каждое наблюдаемое значение однозначно
    классифицируется: либо база с присутствующей в документе дельтой,
    либо чья-то дельта. Неразобранные и пересекающиеся значения (цепочки
    вида 27/28/29) делают раскладку неоднозначной — тогда None.
    """
    values = set(counter)
    zeros: set[str] = set()
    ones: set[str] = set()
    for value in values:
        if value in ones:
            continue
        shifted = shifted_value(param, value)
        if shifted is not None and shifted in values and shifted not in zeros:
            zeros.add(value)
            ones.add(shifted)
    if not ones or zeros & ones or (zeros | ones) != values:
        return None
    return FormattingMethod(
        param=param,
        zero_value=max(zeros, key=lambda v: counter[v]),
        one_value=max(ones, key=lambda v: counter[v]),
        one_values=frozenset(ones),
    )


def _signal_strength(
    chars: list[FormattedChar],
    method: FormattingMethod,
) -> int:
    return sum(
        1
        for c in chars
        if method.is_one(c.attrs.get(method.param))
    )
