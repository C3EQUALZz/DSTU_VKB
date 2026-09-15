"""Общая дельта форматирования для встраивания и распознавания битов."""

from steganography.domain.common.value_objects.formatting_param import FormattingParam


def shifted_value(param: FormattingParam, value: str) -> str | None:
    """Вернуть минимально изменённое значение или None, если сдвиг невозможен.

    Размер задан в half-points, интервал — в twips, масштаб — в процентах.
    Цвет сдвигается на единицу RGB; именованные цвета не поддерживаются.
    У подсветки нет относительной дельты.
    """
    if param is FormattingParam.COLOR:
        if len(value) != 6 or any(char not in "0123456789abcdefABCDEF" for char in value):
            return None
        color = int(value, 16)
        return f"{color + 1:06X}" if color < 0xFFFFFF else None
    if param not in (FormattingParam.SIZE, FormattingParam.SCALE, FormattingParam.SPACING):
        return None
    try:
        number = int(value)
    except ValueError:
        return None
    if param is FormattingParam.SCALE:
        return str(number - 1) if number > 1 else None
    if param is FormattingParam.SIZE and number <= 0:
        return None
    return str(number + 1)
