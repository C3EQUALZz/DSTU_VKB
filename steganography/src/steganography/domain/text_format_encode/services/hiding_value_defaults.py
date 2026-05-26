"""Значения форматирования по умолчанию для каждого параметра сокрытия.

Пары «значение для 0 / значение для 1» подобраны так, чтобы разница была
минимально заметна глазу (как требует методичка): почти одинаковый размер,
почти чёрный цвет, масштаб 100/99 % и т.п. Значения даны в нотации OOXML
(half-points для размера, hex для цвета, проценты для масштаба, twips для
интервала, имена — для подсветки).
"""

from typing import Final

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)

_DEFAULTS: Final[dict[FormattingParam, tuple[str, str]]] = {
    FormattingParam.SIZE: ("28", "29"),
    FormattingParam.COLOR: ("000000", "010000"),
    FormattingParam.HIGHLIGHT: ("white", "yellow"),
    FormattingParam.SCALE: ("100", "99"),
    FormattingParam.SPACING: ("0", "2"),
}


class HidingValueDefaults:
    """Каталог незаметных пар значений для встраивания по параметру."""

    def for_param(self, param: FormattingParam) -> tuple[str, str]:
        return _DEFAULTS[param]
