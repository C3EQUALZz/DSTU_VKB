"""EmbedLsbHammingPresenter — табличный вывод итогов встраивания ПР7."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.lsb_hamming_bmp import (
    EmbedLsbHammingView,
)


@final
class EmbedLsbHammingPresenter:
    """Формирует PrettyTable с метриками внедрения одним из методов ПР7."""

    def render(self, view: EmbedLsbHammingView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"Встраивание ({view.method.human_name})"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Cover-контейнер", str(view.input_image)])
        table.add_row(["Файл-результат", str(view.output_image)])
        table.add_row(["Метод", view.method.human_name])
        stats = view.stats
        table.add_row(["Полезных бит", str(stats.payload_bits)])
        table.add_row(["Доступных слотов LSB", str(stats.capacity_bits)])
        table.add_row(["Изменено каналов", str(stats.changed_channels)])
        table.add_row(["Рейт внедрения", f"{stats.rate:.4f} бит/канал"])
        table.add_row(["Уровень искажений", f"{stats.distortion:.4f}"])
        return table
