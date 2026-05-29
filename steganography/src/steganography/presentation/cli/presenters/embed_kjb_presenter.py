"""EmbedKjbPresenter — табличный вывод результата встраивания КДБ."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.kutter_jordan_bossen import (
    EmbedKjbView,
)


@final
class EmbedKjbPresenter:
    """Формирует PrettyTable с параметрами встраивания КДБ."""

    def render(self, view: EmbedKjbView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"КДБ: встраивание в {view.output_image.name}"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Cover-контейнер", str(view.input_image)])
        table.add_row(["Файл-результат", str(view.output_image)])
        table.add_row(["Сообщение", view.secret_text])
        table.add_row(["Полезных бит", str(view.payload_bits)])
        table.add_row(["Пикселей в контейнере", str(view.container_pixels)])
        table.add_row(["Параметр λ", f"{view.lambda_factor:.3f}"])
        table.add_row(["Seed", str(view.seed)])
        return table
