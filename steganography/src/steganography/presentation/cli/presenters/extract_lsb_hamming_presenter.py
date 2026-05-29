"""ExtractLsbHammingPresenter — табличный вывод итогов извлечения ПР7."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.lsb_hamming_bmp import (
    ExtractLsbHammingView,
)


@final
class ExtractLsbHammingPresenter:
    """Формирует PrettyTable с восстановленным сообщением."""

    def render(self, view: ExtractLsbHammingView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"Извлечение ({view.method.human_name})"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Файл", str(view.input_image)])
        table.add_row(["Метод", view.method.human_name])
        table.add_row(["Восстановленное сообщение", view.message])
        return table
