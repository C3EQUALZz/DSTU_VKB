"""ExtractKjbPresenter — табличный вывод результата извлечения КДБ."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.kutter_jordan_bossen import (
    ExtractKjbView,
)


@final
class ExtractKjbPresenter:
    """Формирует PrettyTable с восстановленным сообщением."""

    def render(self, view: ExtractKjbView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"КДБ: извлечение из {view.input_image.name}"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Файл", str(view.input_image)])
        table.add_row(["Параметр λ", f"{view.lambda_factor:.3f}"])
        table.add_row(["Seed", str(view.seed)])
        table.add_row(["Восстановленное сообщение", view.message])
        return table
