"""FormattingMethod — конкретный метод сокрытия: параметр + значения 0/1."""

from dataclasses import dataclass

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)


@dataclass(frozen=True)
class FormattingMethod:
    """Параметр + два значения, кодирующие биты 0 и 1.

    :attr:`one_values` — необязательное явное множество «единичных»
    значений. Заполняется детектором, когда сокрытие сделано относительной
    дельтой от исходного форматирования и в документе несколько пар
    «база / база+дельта» (разные стили текста в одном контейнере).
    """

    param: FormattingParam
    zero_value: str
    one_value: str
    one_values: frozenset[str] | None = None

    def is_one(self, value: str | None) -> bool:
        if self.one_values is not None:
            return value in self.one_values
        return value == self.one_value

    def describe(self) -> str:
        return (
            f"{self.param.human_name}: для нулей — «{self.zero_value}», "
            f"для единиц — «{self.one_value}»"
        )
