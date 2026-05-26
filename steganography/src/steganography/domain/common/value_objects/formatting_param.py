"""FormattingParam — параметр форматирования docx, носитель скрытого бита."""

from enum import Enum


class FormattingParam(str, Enum):
    """Поддерживаемые параметры форматирования docx-документа."""

    COLOR = "color"
    HIGHLIGHT = "highlight"
    SIZE = "size"
    SCALE = "scale"
    SPACING = "spacing"

    @property
    def human_name(self) -> str:
        return _HUMAN_NAMES[self]


_HUMAN_NAMES: dict[FormattingParam, str] = {
    FormattingParam.COLOR: "цвет символов",
    FormattingParam.HIGHLIGHT: "цвет фона",
    FormattingParam.SIZE: "размер шрифта",
    FormattingParam.SCALE: "масштаб шрифта",
    FormattingParam.SPACING: "межсимвольный интервал",
}
