"""ExtractLsbBmpPresenter — табличный вывод итогов извлечения LSB+Виженер."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.lsb_bmp_vigenere import (
    ExtractLsbBmpView,
)


@final
class ExtractLsbBmpPresenter:
    """Формирует PrettyTable с восстановленным сообщением из BMP."""

    def render(self, view: ExtractLsbBmpView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"Извлечение из {view.input_image.name}"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Файл", str(view.input_image)])
        table.add_row(["Байт шифротекста", str(view.ciphertext_bytes)])
        table.add_row(["Восстановленное сообщение", view.plaintext])
        return table
