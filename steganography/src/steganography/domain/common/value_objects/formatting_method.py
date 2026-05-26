"""FormattingMethod — конкретный метод сокрытия: параметр + значения 0/1."""

from dataclasses import dataclass

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)


@dataclass(frozen=True)
class FormattingMethod:
    """Параметр + два значения, кодирующие биты 0 и 1."""

    param: FormattingParam
    zero_value: str
    one_value: str

    def describe(self) -> str:
        return (
            f"{self.param.human_name}: для нулей — «{self.zero_value}», "
            f"для единиц — «{self.one_value}»"
        )
