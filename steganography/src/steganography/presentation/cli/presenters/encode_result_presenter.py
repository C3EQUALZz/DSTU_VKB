"""EncodeResultPresenter — табличное представление результата встраивания."""

from typing import final

from prettytable import PrettyTable

from steganography.application.common.views.text_format_encode import (
    EncodeSecretView,
)


@final
class EncodeResultPresenter:
    """Формирует PrettyTable-блок с итогом встраивания сообщения."""

    def render(self, view: EncodeSecretView) -> PrettyTable:
        table: PrettyTable = PrettyTable()
        table.title = f"Встраивание в {view.output_path.name}"
        table.field_names = ["Поле", "Значение"]
        table.align["Поле"] = "l"
        table.align["Значение"] = "l"
        table.add_row(["Файл-результат", str(view.output_path)])
        table.add_row(["Сообщение", view.secret_text])
        table.add_row(["Кодировка", view.encoding_name])
        if view.method is not None:
            table.add_row(["Параметр", view.method.param.human_name])
            table.add_row(["Значение для 0", view.method.zero_value])
            table.add_row(["Значение для 1", view.method.one_value])
        if not view.success:
            table.add_row(["Статус", f"ошибка: {view.error}"])
            return table
        table.add_row(["Полезных бит", str(view.payload_bits)])
        table.add_row(["Символов в контейнере", str(view.container_chars)])
        table.add_row(["Статус", "успешно"])
        return table
