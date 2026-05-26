"""DetectResultPresenter — табличное представление результата по одному файлу."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.text_format_decode import (
    DetectSecretView,
)


@final
class DetectResultPresenter:
    """Формирует PrettyTable-блок с подробностями анализа контейнера."""

    def render(self, view: DetectSecretView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"Анализ контейнера {view.docx_path.name}"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Файл", str(view.docx_path)])

        if not view.success or view.method is None or view.encoding is None:
            table.add_row(["Статус", f"ошибка: {view.error}"])
            return table

        table.add_row(["Параметр форматирования", view.method.param.human_name])
        table.add_row(["Атрибут docx", f"w:{view.method.param.value}"])
        table.add_row(["Значение для 0", view.method.zero_value])
        table.add_row(["Значение для 1", view.method.one_value])
        table.add_row(["Кодировка", view.encoding.name])
        table.add_row(["Длина битовой строки", str(len(view.bit_sequence))])
        table.add_row(["Сообщение", view.message.strip()])
        return table
