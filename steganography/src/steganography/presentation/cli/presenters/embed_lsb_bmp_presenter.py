"""EmbedLsbBmpPresenter — табличный вывод итогов встраивания LSB+Виженер."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.lsb_bmp_vigenere import (
    EmbedLsbBmpView,
)


@final
class EmbedLsbBmpPresenter:
    """Формирует PrettyTable с параметрами встраивания сообщения в BMP."""

    def render(self, view: EmbedLsbBmpView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"Встраивание в {view.output_image.name}"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Cover-контейнер", str(view.input_image)])
        table.add_row(["Файл-результат", str(view.output_image)])
        table.add_row(["Байт открытого текста", str(view.plaintext_bytes)])
        table.add_row(["Байт шифротекста", str(view.ciphertext_bytes)])
        table.add_row(["Полезных бит (с метками)", str(view.payload_bits)])
        table.add_row(["Ёмкость контейнера (бит)", str(view.capacity_bits)])
        ratio = view.payload_bits / view.capacity_bits if view.capacity_bits else 0.0
        table.add_row(["Использовано ёмкости", f"{ratio:.2%}"])
        return table
